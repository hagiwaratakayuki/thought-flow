from pydantic import BaseModel
from .overview import TextOverView
from typing import Literal

class TextOverViews(BaseModel):
    texts:list[TextOverView]
    cursor: str | Literal[False]