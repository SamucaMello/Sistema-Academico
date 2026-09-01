from src.schemas.pagination_schema import PaginationSchema
from src.exceptions.aluno_exception import AlunoException
from src.schemas.aluno_schema import CreateAlunoSchema, UpdateAlunoSchema
from src.models.aluno import Aluno, AlunoRedis
from beanie import PydanticObjectId

from typing import Optional, Union

class AlunoService:
    @staticmethod
    def _redis_get(id: PydanticObjectId) -> Optional[AlunoRedis]:
        try: 
            return AlunoRedis.find(
            AlunoRedis.id == str(id)
        ).first()
        except Exception:
            return None

    @staticmethod
    def _redis_save(aluno: Aluno) -> None:
        data = aluno.model_dump(mode="json")
        data["id"] = str(aluno.id)
        AlunoRedis(
            **data
        ).save().expire(60)




    @classmethod
    def _redis_delete(cls, aluno: Aluno) -> None:
        aluno_redis = cls._redis_get(aluno)

        if aluno_redis:
            aluno_redis.delete()


    @classmethod 
    async def create(cls, aluno:CreateAlunoSchema) -> Aluno:
        if await cls.get_by_email(aluno.email):
            raise AlunoException("Esse e-mail já está cadastrado.")
        if await cls.get_by_RA(aluno.RA):
            raise AlunoException("Esse RA já está cadastrado.")

        novo_aluno = Aluno(**aluno.model_dump())
        cls._redis_save(novo_aluno)
        await novo_aluno.insert()
        return novo_aluno
        
    @classmethod
    async def get_by_email(cls, email:str) -> Aluno:
        print(Aluno.model_fields)
        return await Aluno.find_one(Aluno.email == email)

    @classmethod
    async def get_by_RA(cls, RA:str) -> Aluno:
        return await Aluno.find_one(Aluno.RA == RA)
    
    @classmethod
    async def get_by_id(cls, id: PydanticObjectId):
        redis_aluno = cls._redis_get(id)

        if redis_aluno is not None:
            return redis_aluno

        aluno = await Aluno.get(id)

        if aluno is None:
            raise AlunoException("Aluno não encontrado")

        
        cls._redis_save(aluno)
        return aluno

    @classmethod
    async def update(cls, id:PydanticObjectId, updateschema:UpdateAlunoSchema):
        aluno = await Aluno.get(id)

        updts = updateschema.model_dump(exclude_unset=True)
        await aluno.set(updts)

        cls._redis_save(aluno)
        return aluno
    
    @classmethod
    async def delete(cls, id:PydanticObjectId) -> Aluno:
        aluno = await cls.get_by_id(id)
        if aluno:
            cls._redis_delete(aluno)
            await aluno.delete() 
            return aluno
        raise AlunoException("Aluno não encontrado")

    @classmethod
    async def list_all(cls, pagination:PaginationSchema):
        skip = (pagination.page - 1) * pagination.size
        alunos = await Aluno.find_all(skip = skip, limit=pagination.size).to_list()
        return alunos
