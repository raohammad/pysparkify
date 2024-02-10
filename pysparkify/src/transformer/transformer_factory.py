from abc import abstractstaticmethod
from .transformer import Transformer
from .sql_transformer import SQLTransformer

class TransformerFactory():
    
    @abstractstaticmethod
    def build_transformer(transformer_type: str, config) -> Transformer:
        if transformer_type == "SQLTransformer": 
            return SQLTransformer(config)
        #TODO: Add more sinks to factory
        print(f"Unsupported transformer {transformer_type}")
        return -1
