"""
In provider is an analytic table form of in network rates data containing provider details

"""

from ..table_analytic import TableAnalytic
from pyspark.sql.types import StringType, IntegerType, ArrayType, StructType, StructField


class In_provider(TableAnalytic):

    provider_groups = ArrayType(StructType([
        StructField("npi", ArrayType(StringType()), True),
        StructField("tin", StructType([
            StructField("type", StringType(), True),
            StructField("value", StringType(), True)]), True)]))

    definition = \
        [("sk_entity", IntegerType(), False, "SK of payer entity"),
         ("sk_provider", IntegerType(), False, "SK of provider details"),
         ("provider_groups", provider_groups, True, "Group of providers as organized by publisher"),
         ("location", StringType(), True, "URL of download if not provided in provider_groups")]

