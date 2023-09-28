from datetime import datetime 
from pydantic import BaseModel
class TextEntity(BaseModel):
    published:datetime
    body:str
    author:str
    linked_count:int
    link_to: list[str] | None

    