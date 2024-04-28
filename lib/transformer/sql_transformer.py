from pyspark.sql import SparkSession
from lib.transformer.transformer import Transformer

class SQLTransformer(Transformer):
    def __init__(self, config):
        super().__init__(config)

    def transform(self, spark, sources, sinks):
        # Register temporary tables from source configurations
        for source_config in self.source_configs:
            source_name = source_config['name']
            as_name = source_config['as_name']
            source_df = sources[source_name]
            if source_df is not None:
                source_df.createOrReplaceTempView(as_name)
            else:
                print(f"datafame is None for source: {source_name}")

        transformed_df = None
        for statement_config in self.statement_configs:
            sql = statement_config['sql']
            as_name = statement_config['as_name']
            to_sink = statement_config.get('to_sink', None)

            # Execute the SQL transformation
            transformed_df = spark.sql(sql)
            transformed_df.createOrReplaceTempView(as_name)

            if to_sink is not None:
                # Save the result to the specified sink
                for sink in sinks:
                    if sink.name == to_sink:
                        sink.write(spark, transformed_df)
                        # transformed_df.write.mode("overwrite").format("parquet").save(sink_config['name'])

        return transformed_df
