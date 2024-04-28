from abc import ABC, abstractmethod

class Sink(ABC):
    def __init__(self, config):
        self.name = config['name']

    @abstractmethod
    def write(self, spark, df):
        pass
