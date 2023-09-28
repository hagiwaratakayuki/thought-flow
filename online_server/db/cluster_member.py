from typing import Any
from .model import Model
from datetime import datetime

class ClusterMember(Model):
    cluster_id:Any
    text_id:str
    linked_count:int
    published:datetime
    
    