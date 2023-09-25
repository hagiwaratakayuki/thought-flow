
from fastapi import FastAPI, APIRouter
from .router import routings



def configure(app:FastAPI):
    for prefix, router in routings:
        app.include_router(prefix=prefix, router=router)