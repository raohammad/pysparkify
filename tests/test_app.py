import pytest
from pyspark.sql import SparkSession
import pyspark
from src.app import process_data

@pytest.fixture(scope="module")
def spark_session():
    conf = pyspark.SparkConf().setAppName("test") \
    .set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
    .set("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")

    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    yield spark
    spark.stop()

def test_csv_source_and_sink(spark_session):
    config_path = "./tests/config/csv-source-sink.yml"
    result = process_data(config_path, spark_session)
    # Assert the result or perform other checks

def test_redshift_source_and_sink(spark_session):
    config_path = "./tests/config/redshift-source-redshift-sink.yml"
    result = process_data(config_path, spark_session)
    # Assert the result or perform other checks

def test_s3_source_and_sink(spark_session):
    config_path = "./tests/config/redshift-source-redshift-sink.yml"
    result = process_data(config_path, spark_session)

# Add more test cases for different sources and sinks
