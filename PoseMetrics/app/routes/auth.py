from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# Modelo para o corpo da requisição
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "1234":
        return {"status": "success", "message": "Login successful"}
    return {"status": "error", "message": "Invalid credentials"}
