import argparse
import yaml
from pyspark.sql import SparkSession
import pyspark

# import sources
from source.source import Source
from source.csv_source import CsvSource

# import sinks
from sink.sink import Sink
from sink.csv_sink import CsvSink

# import transformers
from transformer.transformer import Transformer
from transformer.sql_transformer import SQLTransformer

# Initialize lists to store sources, sinks, and transformers
source_list = []
sink_list = []
transformer_list = []

def instantiate_source(config):
    # Instantiate a source based on the source type
    source_type = config['type']
    source_class = globals()[source_type]
    return source_class(config['config'])

def instantiate_sink(config):
    # Instantiate a sink based on the sink type
    sink_type = config['type']
    sink_class = globals()[sink_type]
    return sink_class(config['config'])

def instantiate_transformer(config):
    # Instantiate a transformer based on the transformer type
    transformer_type = config['type']
    transformer_class = globals()[transformer_type]
    return transformer_class(config['config'])

def process_data(config_path, spark):
    # Load configuration from the YAML file
    config = []
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    sources_config = config['source']
    sinks_config = config['sink']
    transformers_config = config['transformer']

    # Instantiate and process each source
    for source_config in sources_config:
        source = instantiate_source(source_config)
        source_list.append(source)
    
    for sink_config in sinks_config:
        sink = instantiate_sink(sink_config)
        sink_list.append(sink)

    # Perform transformations (if needed)
    for transformer_config in transformers_config:
        transformer = instantiate_transformer(transformer_config)
        transformer_list.append(transformer)

    # Create a dictionary to store the DataFrames from different sources
    source_data = {}
    for source in source_list:
        print('reading data for source '+source.name)
        source_data[source.name] = source.read(spark)

    # Execute transformers
    for transformer in transformer_list:
        transformer.transform(spark, source_data, sink_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process data using PySpark")
    parser.add_argument("--config", required=True, help="Path to the configuration YAML file (recipe.yml)")
    args = parser.parse_args()
    
    # Create a Spark session
    conf = pyspark.SparkConf().setAppName("spark-transformer") \
        # .set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
        # .set("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")

    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    process_data(args.config, spark)

    # Stop the Spark session when done
    spark.stop()
