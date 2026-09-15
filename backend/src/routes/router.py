from fastapi import APIRouter
from src.routes.aluno_route import aluno_router
from src.routes.notas_route import notas_router

router  = APIRouter()

router.include_router(aluno_router)
router.include_router(notas_router)