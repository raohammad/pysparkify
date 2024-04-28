import argparse
import yaml
from pyspark.sql import SparkSession
import pyspark
from .context_manager import get_spark_session
from configparser import ConfigParser

# import sources
from lib.source.source_factory import SourceFactory

# import sinks
from lib.sink.sink_factory import SinkFactory

# import transformers
from lib.transformer.transformer_factory import TransformerFactory

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

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Process data using PySpark")
#     parser.add_argument("--config", required=True, help="Path to the configuration YAML file (recipe.yml)")
#     args = parser.parse_args()
    
#     # Create a Spark session
#     conf = pyspark.SparkConf().setAppName("pysparkify") \
#         # .set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
#         # .set("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")

#     spark = SparkSession.builder.config(conf=conf).getOrCreate()

#     process_data(args.config, spark)

#     # Stop the Spark session when done
#     spark.stop()

# def run(recipe_path):
#     # Existing code to run the application using the provided recipe_path
#     print(f"Running with recipe: {recipe_path}")
#     # Example Spark session usage
#     spark = get_spark_session()

def run(recipe_path):
    # Load Spark configurations from file
    config = ConfigParser()
    config.read('config/spark_config.conf')

    # Prepare the Spark config dictionary
    spark_config = {key: value for key, value in config.items('SPARK')}

    # Get Spark session
    spark = get_spark_session(app_name=config.get('SPARK', 'spark.app.name'), config=spark_config)

    process_data(recipe_path, spark)

    # Continue with your application logic, such as loading data, performing transformations, and writing outputs
    # Example: data = spark.read.csv("path/to/your/data.csv")
    # Remember to stop the Spark session when done
    spark.stop()

def main():
    parser = argparse.ArgumentParser(description="Run Pysparkify application")
    parser.add_argument('recipe_path', type=str, help='Path to the recipe YAML file')
    args = parser.parse_args()
    run(args.recipe_path)

if __name__ == "__main__":
    main()