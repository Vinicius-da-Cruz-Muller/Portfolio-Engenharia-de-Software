from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.routes import router as routes_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(routes_router)
