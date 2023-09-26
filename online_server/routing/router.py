
from fastapi import FastAPI, APIRouter
import os

routings:list[tuple[str,APIRouter]] = []



def get_routing_tuple(filepath:str, route:APIRouter):
    global routings
    prefix = os.path.basename(filepath).split('.')[0]
    return prefix, route