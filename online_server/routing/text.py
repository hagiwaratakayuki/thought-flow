from fastapi import APIRouter, status
from .query.text import get_all_as_vertex, get_text_keyword, get_linked_text as linked_text

from .query.cluster import get_clusters_by_text

from routing.return_models.text.overview import TextOverView
from routing.return_models.text.overviews import TextOverViews

from routing.return_models.cluster.overview import ClusterOverView
from routing.return_models.cluster.oveviews import ClusterOverViews
from pydantic import BaseModel

from typing import List
from db.text import Text
from app.error_hundling.status_exception import StatusException





router = APIRouter()
@router.get('/all_as_vertex') 
def all_as_vertex() -> List[TextOverView]:
    return [TextOverView(id=e.id, **e) for e in get_all_as_vertex.fetch()]

class TextFull(BaseModel):
    title: str = ''
    body: str = ''
    published: str = ''
    auther: str = ''
    auther_id: str = ''
    keywords: list[str]
    clustres: list[ClusterOverView] | None
    clustres_next: None | str
    linke_to: list | None
    linked_from: list[TextOverView] | None
    linked_from_next: None | str



@router.get('/entity_all',response_model=TextFull, response_model_exclude_none=True)
def get_entity_all(eid:str)-> TextFull:
    entity = Text.get(id=eid)
    if  entity == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    linke_to = Text.get_multi(entity.get('link_to', None)) 
    keywords = get_text_keyword.fetch(text_id=eid)
    cluster_entities, clusters_next = get_clusters_by_text.fetch(text_id=eid)
    if cluster_entities == None:
        clusters = None
    else:
        clusters = [ClusterOverView(**e) for e in cluster_entities]
    linked_from, linked_from_next = get_text_keyword.fetch(text_id=eid)
    return TextFull(title=entity["title"], 
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

@router.get('/get_clusters',response_model=ClusterOverViews, response_model_exclude_none=True)
def get_clusters(eid:str, cursor:str) -> ClusterOverViews:
    cluster_entities, next_cursor =  get_clusters_by_text.fetch(text_id=eid, cursor=cursor)
    if cluster_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    clusters = [ClusterOverView(id=e.id, **e) for e in cluster_entities] # type: ignore
    return ClusterOverViews(clusters=clusters, cursor=next_cursor)

@router.get('/get_linked_text',response_model=TextOverViews, response_model_exclude_none=True)
def get_linked_text(eid:str, cursor:str) -> TextOverViews:
    text_entities, next_cursor = linked_text.fetch(text_id=eid, cursor=cursor)
    if text_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    texts = [TextOverView(id=e.id, **e) for e in text_entities] # type: ignore
    return TextOverViews(texts=texts, cursor=next_cursor)
    
@router.get('/get_link_to',response_model=List[TextOverViews], response_model_exclude_none=True)
def get_link_to(eids: list[str]) -> List[TextOverView]:
    text_entities = Text.get_multi(eids)
    if text_entities == None: 
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    return [TextOverView(id=e.id, **e) for e in text_entities] # type: ignore
    

