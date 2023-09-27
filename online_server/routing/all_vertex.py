from fastapi import APIRouter
from .query import get_all_vertex
from pydantic import BaseModel
from typing import List

class AllVertex(BaseModel):
    id:str
    year:int
    month:int
    date:int



router = APIRouter()
@router.get('/') 
def api() -> List[AllVertex]:
    return [AllVertex(id=str(e.id), year=e['published'].year, month=e['published'].month, date=e['published'].day) for e in get_all_vertex.fetch()]