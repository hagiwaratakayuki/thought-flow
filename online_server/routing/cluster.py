from fastapi import APIRouter, status

from db.cluster import Cluster
from db.text import Text
from typing import List
from .query.cluster import get_cluster_keyword, get_cluster_member, get_cluster_member_by_publishedrange
from app.error_hundling.status_exception import StatusException
from pydantic import BaseModel
from routing.return_models.text.overview import TextOverView
from routing.return_models.text.overviews import TextOverViews
from .util import picker
from .router import get_routing_tuple

router = APIRouter()

class ClusterFull(BaseModel):
    keywords:list[str]
    members_list:list[TextOverView] | None
    members_list_next:str | None
    member_count:int


@router.get('/entity_all',response_model=ClusterFull, response_model_exclude_none=True)
def get_entity_all(id:int)-> ClusterFull:
    entity = Cluster.get(id=id)
    if entity == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    keywords = get_cluster_keyword.fetch(cluster_id=id)
    members_entities, members_list_next = get_cluster_member.fetch(cluster_id=id)
    members_list: list | None = None
    if members_entities  != None:
        members_list = [TextOverView(mem.id, **mem) for mem in members_entities] # type: ignore
    return ClusterFull(
        keywords=keywords,
        member_count=entity["memebr_count"],
        members_list = members_list, 
        members_list_next=members_list_next    
    )

@router.get('/members', response_model=TextOverViews, response_model_exclude_none=True)
def get_members(id:int, cursor: None | str = None)-> TextOverViews:
    members_entities, members_list_next = get_cluster_member.fetch(cluster_id=id, cursor=cursor)
    if members_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    texts = [TextOverView(**mem) for mem in members_entities]
    return TextOverViews(texts=texts, cursor=members_list_next)

@router.get('/members_by_publishedate', response_model=List[TextOverView], response_model_exclude_none=True)
def get_members_by_publishedate(
        eid:str, 
        start_year:int,
        start_month:int,
        start_date:int,
        end_year:int,
        end_month:int,
        end_date:int,          
        
    ) -> List[TextOverView]:
    
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
    return [TextOverView(id=mem.id, **mem) for mem in members] # type: ignore

routing_tuple = get_routing_tuple(__file__, router)