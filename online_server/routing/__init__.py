
from fastapi import FastAPI, APIRouter
import os

routings:list[tuple[str,APIRouter]] = []



def configure(app:FastAPI):
    for prefix, router in routings:
        app.include_router(prefix=prefix, router=router)