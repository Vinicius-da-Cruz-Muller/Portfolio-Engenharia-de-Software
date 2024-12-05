from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from app.routes.auth import router as auth_router
from app.database import get_db_connection


router = APIRouter(prefix="/home", tags=["home"])

class Paciente(BaseModel):
    id: int
    nome: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    estado_civil: Optional[str] = None
    data_nascimento: Optional[str] = None
    condicao: Optional[str] = None
    inicio_tratamento: Optional[str] = None
    fim_tratamento: Optional[str] = None
    prox_sessao: Optional[str] = None
    hora_prox_sessao: Optional[str] = None

class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    email: Optional[str] = None
    estado_civil: Optional[str] = None
    data_nascimento: Optional[str] = None
    condicao: Optional[str] = None
    inicio_tratamento: Optional[str] = None
    fim_tratamento: Optional[str] = None
    prox_sessao: Optional[str] = None
    hora_prox_sessao: Optional[str] = None

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
                SELECT nome, telefone, ultima_sessao, prox_sessao, hora_prox_sessao
                FROM Pacientes
                WHERE atendente = %s and status = true
                ORDER BY prox_sessao ASC
                LIMIT 10
            """, (email_profissional,))
            pacientes = cur.fetchall()

        return pacientes
    finally:
        conn.close()








@router.get("/{email_profissional}/listar_pacientes")
def obter_pacientes(email_profissional: str):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, nome, email, telefone, endereco, estado_civil, condicao, data_nascimento, inicio_tratamento, fim_tratamento,
                        status, ultima_sessao, prox_sessao, hora_prox_sessao
                FROM Pacientes
                WHERE atendente = %s
                ORDER BY prox_sessao ASC
                LIMIT 10
            """, (email_profissional,))
            pacientes = cur.fetchall()

        return pacientes
    finally:
        conn.close()


@router.put("/{paciente_id}")
def editar_paciente(paciente_id: int, paciente: PacienteUpdate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Cria dinamicamente a lista de campos e valores a serem atualizados
            campos = []
            valores = []
            for campo, valor in paciente.dict(exclude_unset=True).items():
                campos.append(f"{campo} = %s")
                valores.append(valor)
            
            # Certifica-se de que há pelo menos um campo para atualizar
            if not campos:
                raise HTTPException(
                    status_code=400, detail="Nenhum campo válido para atualizar."
                )

            # Adiciona o ID do paciente aos valores
            valores.append(paciente_id)

            # Monta a query dinamicamente
            query = f"""
                UPDATE pacientes
                SET {', '.join(campos)}
                WHERE id = %s
            """
            cur.execute(query, valores)
            conn.commit()

        return {"message": "Paciente atualizado com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@router.post("/{email_profissional}/adicionar_paciente")
def adicionar_paciente(paciente: dict):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Pacientes 
                (nome, telefone, email, estado_civil, data_nascimento, endereco, condicao, inicio_tratamento, fim_tratamento, prox_sessao, hora_prox_sessao, atendente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                paciente['nome'], 
                paciente['telefone'], 
                paciente['email'], 
                paciente['estado_civil'], 
                paciente['data_nascimento'], 
                paciente['endereco'], 
                paciente['condicao'], 
                paciente['inicio_tratamento'], 
                paciente['fim_tratamento'], 
                paciente['prox_sessao'], 
                paciente['hora_prox_sessao'], 
                paciente['atendente']
            ))
            conn.commit()
        return {"message": "Paciente adicionado com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


@router.get("/paciente/{paciente_id}")
def get_paciente(paciente_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome, telefone, email, endereco, estado_civil, data_nascimento, condicao, 
                       inicio_tratamento, fim_tratamento, prox_sessao, hora_prox_sessao
                FROM Pacientes
                WHERE id = %s
            """, (paciente_id,))
            paciente = cur.fetchone()

        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")

        # Retornar os dados como um dicionário
        return {
            "id": paciente[0],
            "nome": paciente[1],
            "telefone": paciente[2],
            "email": paciente[3],
            "endereco": paciente[4],
            "estado_civil": paciente[5],
            "data_nascimento": paciente[6],
            "condicao": paciente[7],
            "inicio_tratamento": paciente[8],
            "fim_tratamento": paciente[9],
            "prox_sessao": paciente[10],
            "hora_prox_sessao": paciente[11],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()



@router.get("/{email_profissional}/exercicios")
def listar_exercicios():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, nome, lado, descricao, angulo_minimo_exercicio, angulo_maximo_exercicio
                FROM Exercicios
                ORDER BY nome ASC
            """)
            exercicios = cur.fetchall()

        if not exercicios:
            raise HTTPException(status_code=404, detail="Nenhum exercício encontrado")

        return exercicios
    finally:
        conn.close()




