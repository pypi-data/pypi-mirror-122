from typing import Union, Optional, List
from pydantic import BaseModel


class Response(BaseModel):
    data : Union[str, int, dict, list]
    model : str
    version : str
    list_metrics : Optional[List[dict]] = []
    topics : Optional[List[str]] = []


class RequestPredict(BaseModel):
    data : Union[str, int, dict, list]
    names : Optional[List[str]] = []
    params : Optional[dict] = {}

    class Config:
        extra = "allow"