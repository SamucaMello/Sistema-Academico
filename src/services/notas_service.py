from typing import Optional, Union

from beanie import PydanticObjectId

from src.enums.notas_enum import NotasEnum
from src.models.notas import Notas, NotasRedis
from src.schemas.notas_schema import CreateNotaSchema, UpdateNotaSchema
from src.services.aluno_service import AlunoService

class NotasService:        
    @staticmethod
    def _redis_get(id: PydanticObjectId) -> Optional[NotasRedis]:
        try: 
            return NotasRedis.find(
                NotasRedis.id == str(id)
            ).first()
        except Exception:
                return None
    
    @staticmethod
    def _redis_save(notas:Notas) -> None:
        data = notas.model_dump(mode="json")
        data["id"] = str(notas.id)
        NotasRedis(**data).save().expire(60)
    
    
    @classmethod
    def _redis_delete(cls, id:PydanticObjectId) -> None:
        aluno_redis = cls._redis_get(id)
    
        if aluno_redis:
            aluno_redis.delete()

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
        aluno        = await AlunoService.get_by_id(nota.aluno)
        media:float  = cls.calcular_media(nota.P1, nota.P2)
        nova_nota    = Notas(
                            aluno_id=aluno,
                            P1 = nota.P1,
                            P2 = nota.P2,
                            media = media,
                            situacao= cls.obter_situacao(media)
                             )
        return await nova_nota.insert()


    @classmethod 
    async def _mongo_get(cls, id:PydanticObjectId) -> Notas:
        if (nota:=Notas.get(id)):
            return nota
        raise NotaException("Nota não encontrada")
    
    @classmethod
    async def get_by_id(cls, id:PydanticObjectId):
        return cls._redis_get(id) or cls._mongo_get(id)

    @classmethod 
    async def update(cls, id:PydanticObjectId, updts:UpdateNotaSchema) -> Notas:
        nota = await cls._mongo_get(id)
        nota = await nota.set(updts.model_dump(exclude_unset=True))
        cls._redis_save(nota)
        return nota 


    

    
    
        