from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Annotated
from redis_om import HashModel, Field


class Aluno(Document):
    RA:Annotated[str, Indexed(unique=True)]
    nome:str
    email:EmailStr
    curso:str 
    semestre:int 


class AlunoRedis(HashModel):
    RA: str 
    nome:str
    email:str
    curso:str
    semestre:int