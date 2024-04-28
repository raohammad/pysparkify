from abc import abstractstaticmethod
from .source import Source
from .csv_source import CsvSource


class SourceFactory():
    
    @abstractstaticmethod
    def build_source(source_type: str, config) -> Source:
        if source_type == "CsvSource": 
            return CsvSource(config)
        #TODO: Add more sinks to factory
        print(f"Unsupported source {source_type}")
        return -1
