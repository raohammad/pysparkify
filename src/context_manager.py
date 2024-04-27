# Handles Spark context creation and management
import pyspark
from pyspark.sql import SparkSession

def get_spark_session(app_name="PysparkifyApp", config=None):
    spark_builder = SparkSession.builder.appName(app_name)
    if config:
        for key, value in config.items():
            spark_builder.config(key, value)
    return spark_builder.getOrCreate()
