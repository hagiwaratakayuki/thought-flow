from fastapi import APIRouter, status

from db.cluster import Cluster
from db.text import Text
from typing import List
from .query.cluster import get_cluster_keyword, get_cluster_member, get_cluster_member_by_publishedrange
from app.error_hundling.status_exception import StatusException
from pydantic import BaseModel
from routing.return_models.text.entity import TextEntity
from routing.return_models.text.entities import TextEntities

router = APIRouter()

class EntityAll(BaseModel):
    keywords:list[str]
    members_list:list[TextEntity] | None
    members_list_next:str | None
    member_count:int


@router.get('/entity_all',response_model=EntityAll, response_model_exclude_none=True)
def get_entity_all(eid:str)-> EntityAll:
    entity = Cluster.get(eid=eid)
    if entity == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    keywords = get_cluster_keyword.fetch(cluster_id=eid)
    members_entities, members_list_next = get_cluster_member.fetch(cluster_id=eid)
    members_list: list | None = None
    if members_entities  != None:
        members_list = [TextEntity(**mem) for mem in members_entities]
    return EntityAll(
        keywords=keywords,
        member_count=entity["memebr_count"],
        members_list = members_list, 
        members_list_next=members_list_next    
    )

@router.get('/members', response_model=TextEntities, response_model_exclude_none=True)
def get_members(eid:str, cursor: None | str = None)-> TextEntities:
    members_entities, members_list_next = get_cluster_member.fetch(cluster_id=eid, cursor=cursor)
    if members_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    texts = [TextEntity(**mem) for mem in members_entities]
    return TextEntities(texts=texts, cursor=members_list_next)

@router.get('/members_by_publishedate', response_model=List[TextEntity], response_model_exclude_none=True)
def get_members_by_publishedate(
        eid:str, 
        start_year:int,
        start_month:int,
        start_date:int,
        end_year:int,
        end_month:int,
        end_date:int,          
        
    ) -> List[TextEntity]:
    
    members =  get_cluster_member_by_publishedrange.fetch(
            cluster_id = eid, 
            start_year=start_year,
            start_month=start_month,
            start_date=start_date,
            end_year=end_year,
            end_month=end_month,
            end_date=end_date,          
    )
    if members == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    return [TextEntity(**mem) for mem in members]

