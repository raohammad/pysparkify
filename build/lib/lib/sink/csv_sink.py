from pyspark.sql import SparkSession
from lib.sink.sink import Sink

class CsvSink(Sink):
    def __init__(self, config):
        super().__init__(config)
        self.output_path = config['path']

    def write(self, spark, df):
        # spark = SparkSession.builder.appName("frdspark").getOrCreate()
        df.write.csv(self.output_path, header=True, mode='overwrite')
        # spark.stop()
