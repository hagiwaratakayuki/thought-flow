from pydantic import BaseModel
from .overview import TextOverView

class TextOverViews(BaseModel):
    texts:list[TextOverView]
    cursor: str | None