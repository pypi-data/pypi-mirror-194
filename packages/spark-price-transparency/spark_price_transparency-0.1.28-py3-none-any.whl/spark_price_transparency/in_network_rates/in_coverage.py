"""
In coverage is an analytic table form of in network rate data containing coverage details

"""


from ..table_analytic import TableAnalytic
from pyspark.sql.types import StringType, IntegerType, StructType, StructField, ArrayType


class In_coverage(TableAnalytic):

    planType = StructType([StructField("issuer_name", StringType(), True),
                           StructField("id_type", StringType(), True),
                           StructField("id", StringType(), True),
                           StructField("market_type", StringType(), True)])

    billingCodeType = StructType([StructField("code", StringType(), True),
                                  StructField("type", StringType(), True),
                                  StructField("version", StringType(), True)])

    billingCodesType = ArrayType(billingCodeType)

    definition = \
        [("sk_entity",             IntegerType(),    False, "SK of payer entity"),
         ("sk_date",               StringType(),     True,  "SK of date"),
         ("sk_coverage",           IntegerType(),    True,  "SK of coverage details and primary key for in_coverage"),
         ("version",               StringType(),     True,  "Schema Version"),
         ("reporting_entity_name", StringType(),     True,  "Legal name of the entity publishing"),
         ("reporting_entity_type", StringType(),     True,  "Type of the legal entity"),
         ("plan",                  planType,         True,  "Plan details"),
         ("arrangement",           StringType(),     True,  "ffs, bundle, or capitation"),
         ("name",                  StringType(),     True,  "This is name of the item/service that is offered"),
         ("issuer_billing_code",   billingCodeType,  True,  "Issuer billing code details"),
         ("billing_codes",         billingCodesType, True,  "Array of billing code details")]
