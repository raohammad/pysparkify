from abc import abstractstaticmethod
from .sink import Sink
from .csv_sink import CsvSink

# Sink factory - returns related sink
class SinkFactory():

    @abstractstaticmethod
    def build_sink(sink_type: str, config) -> Sink:
        if sink_type == "CsvSink": 
            return CsvSink(config)
        #TODO: Add more sinks to factory
        print(f"Unsupported sink {sink_type}")
        return -1
