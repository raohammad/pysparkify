from abc import ABC, abstractmethod

class Source(ABC):
    def __init__(self, config):
        self.name = config['name']
    
    @abstractmethod
    def read(self, spark):
        pass
