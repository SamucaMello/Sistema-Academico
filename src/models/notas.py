from beanie import Document, Link
from redis_om import HashModel

from src.models.aluno import Aluno


class Notas(Document):
    aluno_id: Link[Aluno]
    P1: float   
    P2: float 
    media: float       # (P1 + P2) / 2
    situacao:str       # consult. NotasEnum

class NotasRedis(HashModel):
    aluno_id:str
    P1: float
    P2: float 
    media: float 
    situacao:str