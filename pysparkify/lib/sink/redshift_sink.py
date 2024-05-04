from pyspark.sql import SparkSession
from .sink import Sink
from pyspark.sql import DataFrame
import os

class RedshiftSink(Sink):
    def __init__(self, config):
        super().__init__(config)
        self.host = os.environ.get(config['connection']['host'])
        self.port = os.environ.get(config['connection']['port'])
        self.dbname = os.environ.get(config['connection']['dbname'])
        self.dbuser = os.environ.get(config['connection']['dbuser'])
        self.dbpassword = os.environ.get(config['connection']['dbpassword'])
        self.dbtable = config['dbtable']

    def write(self, spark, data: DataFrame):
        # Write data to Amazon Redshift
        data.write \
            .format("jdbc") \
            .option("driver", "com.amazon.redshift.jdbc.Driver") \
            .option("url", f"jdbc:redshift://{self.host}:{self.port}/{self.dbname}") \
            .option("dbtable", self.dbtable) \
            .option("user", self.dbuser) \
            .option("password", self.dbpassword) \
            .mode("append") \
            .save()