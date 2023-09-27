
from fastapi import APIRouter
import os

routings:list[tuple[str,APIRouter]] = []



def get_routing_tuple(filepath:str, route:APIRouter):
    prefix = os.path.basename(filepath).split('.')[0]
    return prefix, route