from abc import ABC, abstractmethod

class Transformer(ABC):
    def __init__(self, config):
        self.name = config['name']
        self.statement_configs = config['statement']
        self.source_configs = config['source']

    @abstractmethod
    def transform(self, spark, sources, sinks):
        pass
