from http import HTTPStatus

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.schemas.pagination_schema import PaginationSchema
from src.services.aluno_service import AlunoService
from src.schemas.aluno_schema import CreateAlunoSchema, UpdateAlunoSchema

aluno_router = APIRouter(prefix = "/aluno", tags=["Rota dos alunos"])

@aluno_router.post("/", status_code=HTTPStatus.CREATED)
async def create(aluno:CreateAlunoSchema):
    aluno = await AlunoService.create(aluno)
    return {"message": "Aluno cadastrado com sucesso!", "aluno":aluno}
    
@aluno_router.get("/{id}", status_code=HTTPStatus.OK)
async def get(id:PydanticObjectId):
    aluno = await AlunoService.get_by_id(id)
    return {"aluno": aluno}

@aluno_router.put("/{id}", status_code=HTTPStatus.OK)
async def update(id:PydanticObjectId, updates:UpdateAlunoSchema):
    aluno = await AlunoService.update(id, updates)
    return  {
        "message": "Aluno atualizado com sucesso!", 
        "aluno":aluno
        }

@aluno_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete(id: PydanticObjectId):
    aluno = await AlunoService.delete(id)
    return {
        "message": "Aluno apagado com sucesso!",
        "aluno": aluno
        }

@aluno_router.get("/", status_code = HTTPStatus.OK)
async def list_alunos(pagination:PaginationSchema = Depends()):
    return await AlunoService.list_all(pagination)