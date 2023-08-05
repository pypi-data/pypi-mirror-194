from pyspark.sql.session import SparkSession
from datetime import date
from .pt_raw import PTRaw
from .pt_stage import PTStage

class Guide:

    spark: SparkSession
    mth: int
    pt_raw: PTRaw

    def __init__(self, mth=None):
        """

        :param mth: INT identifying which month the guide is set
        """
        self.spark = SparkSession.builder.getOrCreate()
        self.mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self.pt_raw = PTRaw()
        self.pt_stage = PTStage()


