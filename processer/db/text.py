from .model import Model
import json
from datetime import datetime
class Text(Model):
    body:str
    title:str
    data:str
    link_to:list[str]
    linked_count:int
    published:datetime
     
    def __init__(self, *args, **kwargs) -> None:
        self._entity_options = { "exclude_from_indexes":("data","body", "title", )}
        super(Text,self).__init__(*args, **kwargs)
    def setProperty(self, body, title, data, linked_to:list[str], linked_count:int, published:datetime):
        self.body = body
        self.title = title
        self.link_to = linked_to
        self.published = published
        self.data = json.dumps(data)
        
