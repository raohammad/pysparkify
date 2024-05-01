from abc import abstractstaticmethod
from .source import Source
from .csv_source import CsvSource
from .s3_source import S3Source
from .redshift_source import RedshiftSource


class SourceFactory():
    
    @abstractstaticmethod
    def build_source(source_type: str, config) -> Source:
        if source_type == "CsvSource": 
            return CsvSource(config)
        elif source_type == "S3Source":
            return S3Source(config)
        elif source_type == "RedshiftSource":
            return RedshiftSource(config)
        #TODO: Add more sinks to factory
        print(f"Unsupported source {source_type}")
        return -1
