from beanie import PydanticObjectId
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.services.aluno_service import AlunoService
from src.schemas.aluno_schema import CreateAlunoSchema

aluno_router = APIRouter("/aluno")

@aluno_router.post("/")
async def create(aluno:CreateAlunoSchema):
    aluno = await AlunoService.create(aluno)
    return JSONResponse(content = dict(
        message = "Aluno criado com sucesso!",
        aluno = aluno
    ))
    
@aluno_router.get("/{id}")
async def get_aluno_by_id(id:PydanticObjectId):
    aluno = AlunoService.get_by_id(id)
    return JSONResponse(content = aluno)


