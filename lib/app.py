import argparse
import yaml
from pyspark.sql import SparkSession
import pyspark
from .context_manager import get_spark_session
from configparser import ConfigParser

# import sources
from pysparkify.lib.source.source_factory import SourceFactory

# import sinks
from pysparkify.lib.sink.sink_factory import SinkFactory

# import transformers
from pysparkify.lib.transformer.transformer_factory import TransformerFactory

# Initialize lists to store sources, sinks, and transformers
source_list = []
sink_list = []
transformer_list = []

def instantiate_source(config):
    # Instantiate a source based on the source type
    source_type = config['type']
    return SourceFactory.build_source(source_type, config['config'])

def instantiate_sink(config):
    # Instantiate a sink based on the sink type
    sink_type = config['type']
    return SinkFactory.build_sink(sink_type, config['config'])

def instantiate_transformer(config):
    # Instantiate a transformer based on the transformer type
    transformer_type = config['type']
    return TransformerFactory.build_transformer(transformer_type, config['config'])

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

def run(recipe_path, spark_config_path='config/spark_config.conf'):
    # Load Spark configurations from file
    config = ConfigParser()
    config.read(spark_config_path)  # Use the provided or default path

    # Prepare the Spark config dictionary
    spark_config = {key: value for key, value in config.items('SPARK')}

    # Get Spark session
    spark = get_spark_session(app_name=config.get('SPARK', 'spark.app.name'), config=spark_config)

    process_data(recipe_path, spark)

    # Remember to stop the Spark session when done
    spark.stop()

def main():
    parser = argparse.ArgumentParser(description="Run Pysparkify application")
    parser.add_argument('recipe_path', type=str, help='Path to the recipe YAML file')
    parser.add_argument('--spark_config', type=str, help='Path to the Spark configuration file', default='config/spark_config.conf')
    args = parser.parse_args()
    run(args.recipe_path, args.spark_config)

if __name__ == "__main__":
    main()