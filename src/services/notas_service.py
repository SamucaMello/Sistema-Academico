from beanie import PydanticObjectId

from enums.notas_enum import NotasEnum
from models.notas import Notas
from src.schemas.notas_schema import CreateNotaSchema
from src.services.aluno_service import AlunoService

class NotasService:
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
    async def get_by_id(cls, id:PydanticObjectId):
        
        