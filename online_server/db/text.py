from .model import Model
import json
class Text(Model):
    body:str
    title:str
    data:str
    link_to:list[str]
    linked_count:int
    published:str
   
    def __init__(self) -> None:
        self._entity_options = { "exclude_from_indexes":("data",)}
        super(Text,self).__init__()
    def setProperty(self, body, title, data, linked_to:list[str], published:str, link_count:int):
        self.body = body
        self.title = title
        self.link_to = linked_to
        self.published = published
        self.data = json.dumps(data)
        
