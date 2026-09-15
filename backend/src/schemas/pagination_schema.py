from typing import List, Union

from beanie import Document
from pydantic import BaseModel,Field


class PaginationSchema(BaseModel):
    page:int = Field(ge=1,          default_factory=1)
    size:int = Field(ge=1, le=25,   default_factory=5)


class PaginationOut[T](BaseModel):
    items:  List[T]
    total:  int
    page:   int 
    size:   int
    pages:  int