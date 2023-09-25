#todo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routing
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
routing.configure(app)
@app.get("/")
def Hello():
    return {"Hello":"World!"}