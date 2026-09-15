from beanie import PydanticObjectId
from pydantic import BaseModel

class CreateNotaSchema(BaseModel):
    aluno: PydanticObjectId
    P1: float 
    P2: float 
    #media: float
    #situacao: str   

class UpdateNotaSchema(BaseModel):
    P1:float
    P2:float
