from .model import Model
from google.cloud.datastore.key import Key
class Cluster(Model):
    title:str
    member_count:int
