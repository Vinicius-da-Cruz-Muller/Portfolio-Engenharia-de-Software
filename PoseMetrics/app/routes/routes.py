from fastapi import APIRouter
from app.routes.auth import router as auth_router

router = APIRouter()

# Inclui as rotas de auth
router.include_router(auth_router)

# No futuro, adicione outras rotas aqui
