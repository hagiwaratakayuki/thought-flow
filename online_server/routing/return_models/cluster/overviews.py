from pydantic import BaseModel
from .overview import ClusterOverView

class ClusterOverViews(BaseModel):
    clusters:list[ClusterOverView]
    cursor: str | None