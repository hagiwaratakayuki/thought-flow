from typing import Any
from .model import Model
from datetime import datetime

class ClusterMember(Model):
    cluster:Any
    text:str
    connect_count:int
    published:datetime
    