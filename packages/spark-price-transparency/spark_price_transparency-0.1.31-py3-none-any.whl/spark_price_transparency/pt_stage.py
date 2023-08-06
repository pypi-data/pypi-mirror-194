
from pyspark.sql.session import SparkSession
from .table_stream_tgt import TableStreamTgt
from .table_analytic import TableAnalytic
from datetime import date

from .in_network_rates.inr_header import Inr_header
from .in_network_rates.inr_network import Inr_network
from .in_network_rates.inr_provider import Inr_provider

from typing import Callable

import time

class PTStage:
    name: str = "pt_stage"
    ingest_tables: {str: TableStreamTgt}
    analytic_tables: {str: TableAnalytic}

    def __init__(self, mth: int = None, spark=None):
        self.spark = spark if spark is not None else SparkSession.builder.getOrCreate()
        self.mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self.ingest_tables = {'inr_header': Inr_header(self.spark),
                              'inr_network': Inr_network(self.spark),
                              'inr_provider': Inr_provider(self.spark)}

    def create_stage_database(self):
        # TODO: check if database already exists
        self.spark.sql(f'CREATE DATABASE IF NOT EXISTS {self.name}')

    def initialize_pt_stage(self):
        self.create_stage_database()
        self.create_ingest_tables()

    def create_ingest_tables(self):
        for ingest_table in self.ingest_tables.values():
            ingest_table.create_table()
            print(ingest_table.tbl_name + " created.")

    def create_analytic_tables(self):
        for ingest_table in self.ingest_tables.values():
            ingest_table.create_table()
            print(ingest_table.tbl_name + " created.")

    def _remove_pt_stage(self):
        """
        Removes all components of pt_stage. Helpful to clean up env after evaluating
        """
        pass

    def get_insertIntoInr(self):
        merge_header: Callable = self.ingest_tables['inr_header'].get_batch_merge_function()
        merge_network: Callable = self.ingest_tables['inr_network'].get_batch_merge_function()
        merge_provider: Callable = self.ingest_tables['inr_provider'].get_batch_merge_function()

        def insertIntoInr(microBatchOutputDF, batchId):
            # This approach feels expensive, will need to compare vs persist & filter
            # header_key = microBatchOutputDF.select('header_key').first()['header_key']
            microBatchOutputDF.persist()
            merge_header(microBatchOutputDF, batchId)
            merge_network(microBatchOutputDF, batchId)
            merge_provider(microBatchOutputDF, batchId)
            microBatchOutputDF.unpersist()
        return insertIntoInr

    def inr_file_query(self, inr_file_path):
        # TODO: make queryName include payer description from file name
        # TODO: derive checkpoint location from raw file location
        source_cp = 'dbfs:/tmp/inr/_checkpoint'
        return self.spark.readStream.option("buffersize", 67108864).format("payer-mrf") \
                   .option("payloadAsArray", "true").load(inr_file_path) \
                   .writeStream.queryName("payer-mrf") \
                   .option("checkpointLocation", source_cp) \
                   .foreachBatch(self.get_insertIntoInr()).start()

    def run_await_ingest_inr_file(self, inr_file_path):
        # Method for single file ingest stop stream on complete
        def stop_on_file_complete(query, wait_time=10):
            while query.isActive:
                msg, is_data_available, is_trigger_active = query.status.values()
                if not is_data_available and not is_trigger_active and msg != "Initializing sources":
                    query.stop()
                time.sleep(5)
            query.awaitTermination(wait_time)
        stop_on_file_complete(self.inr_file_query(inr_file_path), wait_time=10)
