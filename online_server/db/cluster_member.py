from typing import Any
from .model import Model


class ClusterMember(Model):
    cluster:Any
    vertex:Any
    connect:int
    