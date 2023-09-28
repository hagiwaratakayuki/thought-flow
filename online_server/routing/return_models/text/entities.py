from pydantic import BaseModel
from .entity import TextEntity

class TextEntities(BaseModel):
    texts:list[TextEntity]
    cursor: str | None