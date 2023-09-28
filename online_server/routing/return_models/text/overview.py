from datetime import datetime 
from pydantic import BaseModel
class TextOverView(BaseModel):
    id: str | int
    published:datetime
    body:str
    author:str
    linked_count:int
    link_to: list[str] | None

    