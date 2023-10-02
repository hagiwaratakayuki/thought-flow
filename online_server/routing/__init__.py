
from fastapi import FastAPI, APIRouter
from routing import cluster, text


routings:list[tuple[str,APIRouter]] = [
    cluster.routing_tuple,
    text.routing_tuple
]



def configure(app:FastAPI):
    for prefix, router in routings:
        app.include_router(prefix=prefix, router=router)