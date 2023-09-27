from fastapi import APIRouter
from .query import get_all_vertex
from pydantic import BaseModel
from typing import List

class AllVertex(BaseModel):
    


router = APIRouter()
@router.get('/',)
def api():
    pass