from db.model import put_multi
#wiptodo
class Model:

    def __init__(self, chunk_limit=30) -> None:
        self._chunk = []
        self._chunk_limit = chunk_limit
       
    def save(self, model):
        

        self._chunk.append(model)
        
        if len(self._chunk) < 30:
            return
    def _on_save(self):
        entities = put_multi(self._chunk)
        return entities
        

    
    