from pysparkify.lib.source.source import Source
from pyspark.sql.functions import input_file_name, expr

class S3Source(Source):
    def __init__(self, config):
        super().__init__(config)
        self.bucket_name = config['bucket_name']
        self.file_path = config['file_path']
        self.file_type = config['file_type']

    def read(self, spark):
        # Create an S3 path
        s3_path = f"s3a://{self.bucket_name}/{self.file_path}"
        print('here is the path :', s3_path)
        df = None
        # Read data from S3
        try:
            if (self.file_type=='csv'):
                df = spark.read.csv(path=s3_path, header=True, inferSchema=True, encoding="ISO-8859-1" ).withColumn("file_name", expr("substring_index(input_file_name(), '/', -1)"))
            elif (self.file_type=='json'):
                df = spark.read.json(path=s3_path).withColumn("file_name",  expr("substring_index(input_file_name(), '/', -1)"))
            elif (self.file_type=='avro'):
                df = spark.read.avro(path=s3_path).withColumn("file_name",  expr("substring_index(input_file_name(), '/', -1)"))
            elif (self.file_type=='parquet'):
                df = spark.read.avro(path=s3_path).withColumn("file_name",  expr("substring_index(input_file_name(), '/', -1)"))
            else:
                raise MangabeyException(f"No implementation for S3Source file type {self.file_type}")
        except Exception as e:
            print("Custom exception caught:", e)
        return df


