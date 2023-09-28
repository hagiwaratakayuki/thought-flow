from fastapi import APIRouter, status
from .query.text import get_all_as_vertex, get_text_keyword
from .query.cluster import get_clusters_by_text
from pydantic import BaseModel

from typing import List
from db.text import Text
from app.error_hundling.status_exception import StatusException

class AsVertex(BaseModel):
    id:str
    link_to:List[str]
    year:int
    month:int
    date:int



router = APIRouter()
@router.get('/all_as_vertex') 
def all_as_vertex() -> List[AsVertex]:
    return [AsVertex(id=str(e.id),
                      year=e['published'].year, 
                      month=e['published'].month, 
                      date=e['published'].day, 
                      link_to=e['link_to']) 
            for e in get_all_as_vertex.fetch()]

class EntityAll(BaseModel):
    title: str = ''
    body: str = ''
    published: str = ''
    auther: str = ''
    auther_id: str = ''
    keywords: list[str]
    clustres: list | None
    clustres_next: None | str
    linke_to: list | None
    linked_from: list | None
    linked_from_next: None | str



@router.get('/entity_all',response_model=EntityAll, response_model_exclude_none=True)
def get_entity_all(eid:str)-> EntityAll:
    entity = Text.get(eid=eid)
    if  entity == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    linke_to = Text.get_multi(entity.get('link_to', None)) 
    keywords = get_text_keyword.fetch(text_id=eid)
    clusters, clusters_next = get_clusters_by_text.fetch(text_id=eid)
    linked_from, linked_from_next = get_text_keyword.fetch(text_id=eid)
    return EntityAll(title=entity["title"], 
                    body=entity["body"],
                    published=entity["published"],
                    auther=entity["auther"],
                    auther_id=entity["author_id"],
                    linke_to=linke_to,
                    clustres=clusters,
                    clustres_next=clusters_next,
                    keywords=keywords,
                    linked_from=linked_from,
                    linked_from_next=linked_from_next



        )





    

