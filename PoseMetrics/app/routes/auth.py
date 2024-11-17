from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.hash import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/auth", tags=["auth"])

class User(BaseModel):
    nome: str
    email: str
    senha: str

def get_db_connection():
    conn = psycopg2.connect(
        dbname="PoseMetrics",  
        user="postgres",  
        password="18080812", 
        host="localhost", 
        port="5433" 
    )
    return conn

@router.post("/cadastro")
def register(user: User):
    # Verifica se o e-mail já existe
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Acessos WHERE email = %s", (user.email,))
            existing_user = cur.fetchone()

            if existing_user:
                raise HTTPException(status_code=400, detail="E-mail já cadastrado")

            hashed_password = bcrypt.hash(user.senha)  
            cur.execute(
                "INSERT INTO Acessos (nome_completo, email, senha) VALUES (%s, %s, %s)",
                (user.nome, user.email, hashed_password)
            )
            conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade no banco de dados")
    finally:
        conn.close()

    return {"status": "success", "message": "Usuário cadastrado com sucesso"}


@router.post("/login")
def login(email: str, password: str):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM Acessos WHERE email = %s", (email,))
            user = cur.fetchone()

        if not user or not bcrypt.verify(password, user["senha"]):
            raise HTTPException(status_code=400, detail="Credenciais inválidas")

        return {"status": "success", "message": "Login successful"}
    finally:
        conn.close()


@router.get("/teste_conexao")
def teste_conexao():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "success", "message": "Conexão com o banco de dados bem-sucedida."}
    except HTTPException as e:
        return {"status": "error", "message": e.detail}
