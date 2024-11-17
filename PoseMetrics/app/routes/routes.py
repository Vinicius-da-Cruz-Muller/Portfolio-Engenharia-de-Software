from fastapi import APIRouter, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from app.routes.auth import router as auth_router
from app.database import get_db_connection


router = APIRouter(prefix="/home", tags=["home"])

@router.get("/{email_profissional}")
def obter_profissional(email_profissional: str):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT nome_completo, foto FROM Acessos WHERE email = %s", (email_profissional,))
            profissional = cur.fetchone()

            if not profissional:
                raise HTTPException(status_code=404, detail="Profissional não encontrado")

        return profissional
    finally:
        conn.close()

@router.get("/{email_profissional}/proximos_pacientes")
def obter_pacientes(email_profissional: str):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT nome, prox_sessao, hora_prox_sessao
                FROM Pacientes
                WHERE atendente = %s
                ORDER BY prox_sessao ASC
                LIMIT 10
            """, (email_profissional,))
            pacientes = cur.fetchall()

        return pacientes
    finally:
        conn.close()
