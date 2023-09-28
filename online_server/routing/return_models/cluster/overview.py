from pydantic import BaseModel

class ClusterOverView(BaseModel):
    id:str | int
    title:str = ''
    member_count:int
    short_keywords:list[str]
