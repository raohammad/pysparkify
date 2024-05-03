from pyspark.sql import SparkSession
import psycopg2
from .source import Source
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType, BooleanType
import os

class RedshiftSource(Source):
    def __init__(self, config):
        super().__init__(config)
        self.host = os.environ.get(config['connection']['host'])
        self.port = os.environ.get(config['connection']['port'])
        self.dbname = os.environ.get(config['connection']['dbname'])
        self.dbuser = os.environ.get(config['connection']['dbuser'])
        self.dbpassword = os.environ.get(config['connection']['dbpassword'])
        self.statement = config['statement']
        self.infer_schema = config['infer_schema']
        if(self.infer_schema == False):
            self.schema = self.create_schema(config['schema'])

    def read(self, spark):
        # Connect to Redshift and fetch data
        connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.dbuser,
            password=self.dbpassword
        )
        cursor = connection.cursor()
        cursor.execute(self.statement)
        data = cursor.fetchall()
        connection.close()

        # Convert data to a Spark DataFrame (if needed)
        df = self.convert_to_dataframe(data,spark)
        return df

    def convert_to_dataframe(self, data,spark):
        # Assuming data is a list of tuples or a list of lists
        if not data:
            return None

        # Define a list of column names if not available
        # Example: column_names = ['column1', 'column2', 'column3']

        # Create a Spark DataFrame
        # spark = SparkSession.builder.appName("frdspark").getOrCreate()
        if(self.infer_schema == False):
            df = spark.createDataFrame(data,schema=self.schema)
        else:
            df = spark.createDataFrame(data)
        return df
    
    def create_schema(self, config):
        fields = []
        for field_config in config:
            name = field_config['name']
            data_type = self.get_data_type(field_config['type'])
            nullable = field_config.get('nullable', True)
            field = StructField(name, data_type, nullable)
            fields.append(field)
        return StructType(fields)

    def get_data_type(self, type_name):
        data_type_mapping = {
            'string': StringType(),
            'integer': IntegerType(),
            'long': LongType(),
            'timestamp': TimestampType(),
            'boolean': BooleanType()
            # Add more data types as needed
        }
        return data_type_mapping.get(type_name, StringType())