from abc import abstractstaticmethod
from .sink import Sink
from .csv_sink import CsvSink
from .s3_sink import S3Sink
from .redshift_sink import RedshiftSink
from .postgres_sink import PostgresSink

# Sink factory - returns related sink
class SinkFactory():

    @abstractstaticmethod
    def build_sink(sink_type: str, config) -> Sink:
        if sink_type == "CsvSink": 
            return CsvSink(config)
        elif sink_type == "S3Sink":
            return S3Sink(config)
        elif sink_type == "RedshiftSink":
            return RedshiftSink(config)
        elif sink_type == "PostgresSink":
            return PostgresSink(config)
        #TODO: Add more sinks to factory
        print(f"Unsupported sink {sink_type}")
        return -1
