from pydantic import BaseModel,Field


class PaginationSchema(BaseModel):
    page:int = Field(ge=1,          default=1)
    size:int = Field(ge=1, le=25,   default=5)