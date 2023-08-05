"""
In rate is an analytic table form of in network rate data containing rate details

"""
from ..table_analytic import TableAnalytic
from pyspark.sql.types import StringType, IntegerType, ArrayType, FloatType, DateType


class In_rate(TableAnalytic):

    serviceCodeType = ArrayType(StringType())
    billCodeModifierType = ArrayType(StringType())

    definition = \
        [("sk_entity", IntegerType(), False, "SK of payer entity"),
         ("sk_date", StringType(), True, "SK of date"),
         ("sk_coverage", IntegerType(), True, "SK of coverage details"),
         ("sk_provider", IntegerType(), True, "SK of provider details"),
         ("negotiated_type", StringType(), True, "negotiated, derived, fee schedule, percentage, or per diem"),
         ("negotiated_rate", FloatType(), True, "Dollar or percentage based on the negotiation_type"),
         ("expiration_date", DateType(), True, "Date agreement for the negotiated_price ends"),
         ("service_code", serviceCodeType, True, "CMS two-digit code(s) placed on a professional claim"),
         ("billing_class", StringType(), True, "professional or institutional"),
         ("billing_code_modifier", billCodeModifierType, True, "Billing Code Modifiers")]
