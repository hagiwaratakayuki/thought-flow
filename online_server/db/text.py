from .model import Model
import json
class Text(Model):
    body:str
    title:str
    data:str
   
    def __init__(self) -> None:
        self._entity_options = { "exclude_from_indexes":("data",)}
        super(Text,self).__init__()
    def setProperty(self, body, title, data):
        self.body = body
        self.title = title
        self.data = json.dumps(data)
        
