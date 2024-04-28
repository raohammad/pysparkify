from pyspark.sql import SparkSession
from lib.source.source import Source

class CsvSource(Source):
    def __init__(self, config):
        super().__init__(config)
        self.input_path = config['path']

    def read(self, spark):
        # spark = SparkSession.builder.appName("frdspark").getOrCreate()
        df = spark.read.csv(self.input_path, header=True, inferSchema=True)
        # print(df)
        # spark.stop()
        return df
