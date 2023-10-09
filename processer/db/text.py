from .model import Model
import json, math
from datetime import datetime
class Text(Model):
    body:str
    title:str
    data:str
    author:str = ''
    author_id:str = ''
    link_to: list[str] | None
    linked_count:int
    published:datetime
    weight:float
     
    def __init__(self, *args, **kwargs) -> None:
        
        super(Text,self).__init__(entity_options= { "exclude_from_indexes":("data","body", "title", )}, *args, **kwargs)
    def setProperty(self, title, body,  data, linked_to:list[str], linked_count:int, published:datetime, author:str, author_id:str):
        self.body = body
        self.title = title
        self.link_to = linked_to
        self.published = published
        self.data = json.dumps(data)
        self.linked_count = linked_count
        if linked_count == 0:
            weight = 0.0
        else:
            weight = math.log(linked_count) * (float(published.year) + float(published.month) / 100.0 + float(published.day)/ 10000.0) 


        self.weight = weight
        
