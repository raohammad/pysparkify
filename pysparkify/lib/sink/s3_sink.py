from .sink import Sink

class S3Sink(Sink):
    def __init__(self, config):
        super().__init__(config)
        self.bucket_name = config['bucket_name']
        self.file_path = config['file_path']

    def write(self, spark, data):
        # Create an S3 path
        s3_path = f"s3a://{self.bucket_name}/{self.file_path}"

        # Write data to S3
        data.coalesce(1).write.format("csv").mode("overwrite").option("header", "true").save(s3_path)
