import math
from typing import Optional, Union

from beanie import PydanticObjectId

from src.models.aluno import Aluno
from src.schemas.pagination_schema import PaginationOut, PaginationSchema
from src.exceptions.notas_exception import NotasException
from src.enums.notas_enum import NotasEnum
from src.models.notas import Notas, NotasRedis
from src.schemas.notas_schema import CreateNotaSchema, UpdateNotaSchema
from src.services.database_service import DatabaseService


class NotasService:
    db_service = DatabaseService(NotasRedis, Notas)
    
    @staticmethod 
    def calcular_media(*notas:list):
        return sum(notas) / len(notas)
    
    @staticmethod 
    def obter_situacao(media:float):
        if media < 4:
            return NotasEnum.REPROVADO
        if media >= 4 and media < 6:
            return NotasEnum.EXAME
        if media >= 6:
            return NotasEnum.APROVADO
         
    @classmethod
    async def create(cls, nota:CreateNotaSchema):
        
        
        from src.services.aluno_service import AlunoService
        aluno        = await AlunoService.db_service.mongo_get(nota.aluno)
        if await cls.get_by_aluno(aluno):
            raise NotasException("Esse aluno já possui nota.")
        
        media:float  = cls.calcular_media(nota.P1, nota.P2)
        nova_nota    = await Notas(
                            aluno=aluno,
                            P1 = nota.P1,
                            P2 = nota.P2,
                            media = media,
                            situacao = cls.obter_situacao(media).value
                             ).insert()
        await nova_nota.fetch_all_links()
        cls.db_service.redis_save(nova_nota)
        return nova_nota

    
    @classmethod
    async def get_by_id(cls, id:PydanticObjectId):
        redis = cls.db_service.redis_get(id)
        if not redis:
            nota = await cls.db_service.mongo_get(id)
            cls.db_service.redis_save(nota)
            return nota
        
        if not redis:
            raise NotasException("Nota não encontrada")



    @classmethod 
    async def update(cls, id:PydanticObjectId, updts:UpdateNotaSchema) -> Notas:
        nota = await cls.db_service.mongo_get(id)
        if nota is None:
            raise NotasException("Nota não encontrada")
        to_update = updts.model_dump(exclude_unset=True)
        nota = await nota.set(to_update)
        cls.db_service.redis_save(nota)
        return nota 

    @classmethod 
    async def list_all(cls, pagination:PaginationSchema) -> PaginationOut:
        skip = ( pagination.page - 1 ) * pagination.size
        total = await Notas.find_all().count()
        items = await Notas.find_all(skip = skip, limit=pagination.size, fetch_links=True).to_list()
        pages = math.ceil(total / pagination.size) if pagination.size else 0

        return PaginationOut(
                    items=items,
                    pages = pages,
                    total = total,
                    page = pagination.page,
                    size = pagination.size
        )
        

    @classmethod 
    async def delete(cls, id:PydanticObjectId) -> Notas:
        if nota := await cls.db_service.mongo_get(id):
            cls.db_service.redis_delete(id)
            await nota.delete()
            return nota
        raise NotasException("Nota não encontrada")

    @classmethod
    async def get_by_aluno(cls, aluno:Aluno) -> Notas:
        return await Notas.find_one(Notas.aluno.id == aluno.id)


    @classmethod
    async def delete_by_aluno(cls, aluno:Aluno):
        if nota:=await cls.get_by_aluno(aluno):
         await nota.delete()
           