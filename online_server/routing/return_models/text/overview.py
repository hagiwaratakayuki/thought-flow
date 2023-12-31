from datetime import datetime 
from pydantic import BaseModel
class TextOverView(BaseModel):
    id: str | int
    title:str
    published:datetime
    body:str
    author:str
    author_id:str
    linked_count:int
    link_to: list[str | int] | None = None
    position:float | None = None

    