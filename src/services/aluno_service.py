from src.exceptions.aluno_exception import AlunoException
from src.schemas.aluno_schema import CreateAlunoSchema
from src.models.aluno import Aluno, AlunoRedis
from beanie import PydanticObjectId
from src.database.db import RedisManager

class AlunoService:
    @classmethod 
    async def create(cls, aluno:CreateAlunoSchema) -> Aluno:
        if cls.get_by_email(aluno.email):
            raise AlunoException("Esse e-mail já está cadastrado.")
        
        novo_aluno = Aluno(**aluno.model_dump())
        await novo_aluno.insert()
        return novo_aluno
        
    @classmethod
    async def get_by_email(cls, email:str) -> Aluno:
        if AlunoRedis.get(email)
        return await Aluno.find_one(Aluno.email == email)
    
    @classmethod
    async def get_by_id(cls, id:PydanticObjectId):
        if not (aluno := await Aluno.get(id)):
            raise AlunoException("Aluno não encontrado")
        return aluno
    
    @classmethod
    async def delete(cls, id:PydanticObjectId) -> Aluno:
        aluno = await cls.get_by_id(id)
        return aluno.delete() and aluno
        