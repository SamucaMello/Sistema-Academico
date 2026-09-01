from beanie import Document, Indexed
from typing import Annotated
from redis_om import Field, HashModel


class Aluno(Document):
    RA: Annotated[str, Indexed(unique=True)]
    nome:str
    email:str
    curso:str 
    semestre:int 


class AlunoRedis(HashModel, index=True):
    RA: str 
    nome:str
    email:str
    curso:str
    semestre:int
    id:str = Field(index=True)


