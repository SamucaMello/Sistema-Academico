from http import HTTPStatus
import math
from src.services.notas_service import NotasService
from src.services.database_service import DatabaseService
from src.schemas.pagination_schema import PaginationOut, PaginationSchema
from src.exceptions.aluno_exception import AlunoException
from src.schemas.aluno_schema import CreateAlunoSchema, UpdateAlunoSchema
from src.models.aluno import Aluno, AlunoRedis
from beanie import  PydanticObjectId

from typing import Optional, Union

class AlunoService:
    db_service = DatabaseService(AlunoRedis, Aluno)

    @classmethod 
    async def create(cls, aluno:CreateAlunoSchema) -> Aluno:
        if await cls.get_by_email(aluno.email):
            raise AlunoException("Esse e-mail já está cadastrado.")
        if await cls.get_by_RA(aluno.RA):
            raise AlunoException("Esse RA já está cadastrado.")

        novo_aluno = await Aluno(**aluno.model_dump()).insert()
        cls.db_service.redis_save(novo_aluno)
        return novo_aluno
        
    @classmethod
    async def get_by_email(cls, email:str) -> Aluno:
        return await Aluno.find_one(Aluno.email == email)

    @classmethod
    async def get_by_RA(cls, RA:str) -> Aluno:
        return await Aluno.find_one(Aluno.RA == RA)
    
    @classmethod
    async def get_by_id(cls, id: PydanticObjectId):
        redis_get = cls.db_service.redis_get(id)
        if redis_get:
            return redis_get

        mongo_get = await cls.db_service.mongo_get(id)
        if mongo_get:
            cls.db_service.redis_save(mongo_get)
            return mongo_get 


        raise AlunoException("Aluno não encontrado")


    @classmethod
    async def update(cls, id:PydanticObjectId, updateschema:UpdateAlunoSchema):
        aluno = await Aluno.get(id)
        if not aluno:
            raise AlunoException("Aluno não encontrado", status_code=HTTPStatus.NOT_FOUND)

        updts = updateschema.model_dump(exclude_unset=True)
        await aluno.set(updts)

        cls.db_service.redis_save(aluno)
        return aluno
    
    @classmethod
    async def delete(cls, id:PydanticObjectId) -> Aluno:
        aluno = await Aluno.get(id)
        if aluno is None:
            raise AlunoException("Aluno não encontrado", status_code=HTTPStatus.NOT_FOUND)

        await NotasService.delete_by_aluno(aluno)
        await aluno.delete() 
        cls.db_service.redis_delete(aluno.id)
        return aluno

    @classmethod
    async def list_all(cls, pagination:PaginationSchema) -> PaginationOut:
        skip = (pagination.page - 1) * pagination.size

        total = await Aluno.find_all().count()
        items = await Aluno.find_all(skip = skip, limit=pagination.size).to_list()
        pages = math.ceil(total / pagination.size) if pagination.size else 0

        res = PaginationOut[Aluno](
            items = items,
            pages = pages,
            total = total,
            page = pagination.page,
            size = pagination.size
        )
        return res 
