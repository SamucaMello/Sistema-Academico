from http import HTTPStatus

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.models.notas import Notas
from src.schemas.notas_schema import CreateNotaSchema, UpdateNotaSchema
from src.services.notas_service import NotasService
from src.schemas.pagination_schema import PaginationOut, PaginationSchema

notas_router = APIRouter(prefix = "/notas", tags=["Rota das notas"])

@notas_router .post("/", status_code=HTTPStatus.CREATED)
async def create(nota:CreateNotaSchema):
    notas = await NotasService.create(nota)
    return {"message": "Nota criada com sucesso!", "nota":notas}
    
@notas_router .get("/{id}", status_code=HTTPStatus.OK)
async def get(id:PydanticObjectId):
    nota = await NotasService.get_by_id(id)
    return {"nota": nota}

@notas_router .put("/{id}", status_code=HTTPStatus.OK)
async def update(id:PydanticObjectId, updates:UpdateNotaSchema):
    nota = await NotasService.update(id, updates)
    return  {
        "message": "Nota atualizada com sucesso!", 
        "nota":nota
        }

@notas_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete(id: PydanticObjectId):
    nota = await NotasService.delete(id)
    return {
        "message": f"Nota apagada com sucesso!",
        "nota": nota
        }

@notas_router.get("/", status_code = HTTPStatus.OK, response_model=PaginationOut)
async def list_notas(pagination:PaginationSchema = Depends()):
    return await NotasService.list_all(pagination)