from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import error_hundling

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
error_hundling.add_hundler(app=app)