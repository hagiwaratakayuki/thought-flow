from fastapi import APIRouter
from .query.text import get_all_as_vertex
from pydantic import BaseModel
from typing import List

class AsVertex(BaseModel):
    id:str
    link_to:List[str]
    year:int
    month:int
    date:int



router = APIRouter()
@router.get('/all_as_vertex') 
def all_as_vertex() -> List[AsVertex]:
    return [AsVertex(id=str(e.id), year=e['published'].year, month=e['published'].month, date=e['published'].day, link_to=e['link_to']) for e in get_all_as_vertex.fetch()]

