from .model import Model
import datetime
from google.cloud.datastore.key import Key
class Vertex(Model):
    text:Key
    link_to:list[str]
    linked_count:int
    published:str
