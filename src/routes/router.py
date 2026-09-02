from fastapi import APIRouter
from src.routes.aluno_route import aluno_router

router  = APIRouter()

router.include_router(aluno_router)