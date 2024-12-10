from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, Form
from typing import Optional
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from app.routes.auth import router as auth_router
from app.database import get_db_connection
from datetime import date

import base64


router = APIRouter(prefix="/home", tags=["home"])

#Classes MOdelos do Pydantic

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

class ExercicioUpdate(BaseModel):
    nome: Optional[str] = None
    grupo_muscular: Optional[str] = None
    lado: Optional[str] = None
    x1: Optional[float] = None
    x2: Optional[float] = None
    x3: Optional[float] = None
    angulo_minimo_exercicio: Optional[int] = None
    angulo_maximo_exercicio: Optional[int] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None

class ExercicioCreate(BaseModel):
    nome: str
    grupo_muscular: str
    lado: str
    x1: float
    x2: float
    x3: float
    angulo_minimo_exercicio: int
    angulo_maximo_exercicio: int
    descricao: str
    tipo: str


class SessaoPayload(BaseModel):
    paciente_id: int
    massa: float
    altura: float


class ConcluirSessaoPayload(BaseModel):
    sessao_id: int
    tempo_total: float
    observacoes: str

class SeriePayload(BaseModel):
    sessao_id: int
    exercicio_id: int
    numero_serie: int
    tempo: float  
    ponto: str  
    peso: float  
    equipamento: str  
    angulo_coletado: float  



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
            campos = []
            valores = []
            for campo, valor in paciente.dict(exclude_unset=True).items():
                campos.append(f"{campo} = %s")
                valores.append(valor)
            
            if not campos:
                raise HTTPException(
                    status_code=400, detail="Nenhum campo válido para atualizar."
                )

            valores.append(paciente_id)

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
async def adicionar_paciente(
    nome: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(...),
    estado_civil: str = Form(...),
    data_nascimento: str = Form(...),
    endereco: str = Form(...),
    condicao: str = Form(...),
    inicio_tratamento: str = Form(...),
    fim_tratamento: str = Form(...),
    prox_sessao: str = Form(...),
    hora_prox_sessao: str = Form(...),
    atendente: str = Form(...),
    foto: UploadFile = None,
):
    conn = get_db_connection()
    try:
        foto_bytes = await foto.read() if foto else None

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Pacientes 
                (nome, telefone, email, estado_civil, data_nascimento, endereco, condicao, inicio_tratamento, fim_tratamento, prox_sessao, hora_prox_sessao, atendente, foto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nome, 
                telefone, 
                email, 
                estado_civil, 
                data_nascimento, 
                endereco, 
                condicao, 
                inicio_tratamento, 
                fim_tratamento, 
                prox_sessao, 
                hora_prox_sessao, 
                atendente,
                foto_bytes
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
                       inicio_tratamento, fim_tratamento, prox_sessao, hora_prox_sessao, foto
                FROM Pacientes
                WHERE id = %s
            """, (paciente_id,))
            paciente = cur.fetchone()

        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        
        foto_base64 = None
        if paciente[12]:  
            foto_base64 = base64.b64encode(paciente[12]).decode("utf-8")
                    

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
            "foto": foto_base64
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
                SELECT id, nome, grupo_muscular, lado, x1, x2, x3, angulo_minimo_exercicio, angulo_maximo_exercicio, descricao, tipo
                FROM Exercicios
                ORDER BY nome ASC
            """)
            exercicios = cur.fetchall()

        if not exercicios:
            raise HTTPException(status_code=404, detail="Nenhum exercício encontrado")

        return exercicios
    finally:
        conn.close()



@router.put("/{email_profissional}/exercicios/{exercicio_id}")
def editar_exercicio(exercicio_id: int, exercicio: ExercicioUpdate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            campos = []
            valores = []
            for campo, valor in exercicio.dict(exclude_unset=True).items():
                campos.append(f"{campo} = %s")
                valores.append(valor)
            
            if not campos:
                raise HTTPException(
                    status_code=400, detail="Nenhum campo válido para atualizar."
                )

            valores.append(exercicio_id)

            query = f"""
                UPDATE Exercicios
                SET {', '.join(campos)}
                WHERE id = %s
            """
            cur.execute(query, valores)
            conn.commit()

        return {"message": "Exercício atualizado com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()



@router.post("/{email_profissional}/exercicios/criar_exercicio")
def adicionar_exercicio(exercicio: ExercicioCreate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Exercicios 
                (nome, grupo_muscular, lado, x1, x2, x3, angulo_minimo_exercicio, angulo_maximo_exercicio, descricao, tipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                exercicio.nome,
                exercicio.grupo_muscular,
                exercicio.lado,
                exercicio.x1,
                exercicio.x2,
                exercicio.x3,
                exercicio.angulo_minimo_exercicio,
                exercicio.angulo_maximo_exercicio,
                exercicio.descricao,
                exercicio.tipo
            ))
            conn.commit()

        return {"message": "Exercício adicionado com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()



@router.get("/pacientes/{paciente_id}/sessoes")
def listar_sessoes_paciente(paciente_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, paciente_id, data_sessao, tempo_total, observacoes, massa, altura
                FROM Sessoes
                WHERE paciente_id = %s
                ORDER BY data_sessao ASC
            """, (paciente_id,))
            sessoes = cur.fetchall()

        if not sessoes:
            return {"message": "Nenhuma sessão encontrada para o paciente informado."}

        return sessoes
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()



@router.get("/series/filtrar/{sessao_ids}")
def filtrar_series(sessao_ids: str):
    ids = [int(id) for id in sessao_ids.split(',')]  
    
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, sessao_id, exercicio_id, numero_serie, tempo, ponto, peso, equipamento, angulo_coletado
                FROM Serie
                WHERE sessao_id IN %s
            """, (tuple(ids),)) 
            series = cur.fetchall()

        if not series:
            raise HTTPException(status_code=404, detail="Nenhuma série encontrada para os IDs fornecidos.")
        
        return series
    
    finally:
        conn.close()



@router.get("/exercicios/filtrar/{exercicio_ids}")
def filtrar_exercicios(exercicio_ids: str):
    ids = [int(id) for id in exercicio_ids.split(',')] 
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, nome, grupo_muscular, lado, descricao
                FROM Exercicios
                WHERE id in %s
            """, (tuple(ids),))
            exercicios = cur.fetchall()
        
        if not exercicios:
            raise HTTPException(status_code=404, detail="Nenhum exercício encontrado para os IDs fornecidos.")
        
        return exercicios
    
    finally:
        conn.close()



@router.post("/sessoes/iniciar")
def iniciar_ou_atualizar_sessao(payload: SessaoPayload):
    conn = get_db_connection()
    try:
        hoje = date.today() 
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id FROM Sessoes
                WHERE paciente_id = %s AND DATE(data_sessao) = %s
            """, (payload.paciente_id, hoje))
            
            sessao_existente = cur.fetchone()
            
            if sessao_existente:
                sessao_id = sessao_existente["id"]
                cur.execute("""
                    UPDATE Sessoes
                    SET massa = %s, altura = %s
                    WHERE id = %s
                """, (payload.massa, payload.altura, sessao_id))
                conn.commit()
                return {"message": "Sessão atualizada com sucesso.", "sessao_id": sessao_id}
            else:
                cur.execute("""
                    INSERT INTO Sessoes (paciente_id, data_sessao, tempo_total, massa, altura)
                    VALUES (%s, NOW(), %s, %s, %s)
                    RETURNING id
                """, (payload.paciente_id, 0, payload.massa, payload.altura))
                sessao_id = cur.fetchone()["id"]
                conn.commit()
                return {"message": "Nova sessão criada com sucesso.", "sessao_id": sessao_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()



@router.put("/sessoes/concluir")
def concluir_sessao(payload: ConcluirSessaoPayload):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id FROM Sessoes WHERE id = %s", (payload.sessao_id,))
            sessao = cur.fetchone()

            if not sessao:
                raise HTTPException(status_code=404, detail="Sessão não encontrada.")

            cur.execute("""
                UPDATE Sessoes
                SET tempo_total = %s, observacoes = %s
                WHERE id = %s
            """, (payload.tempo_total, payload.observacoes, payload.sessao_id))

            conn.commit()
            return {"message": "Sessão concluída com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()



@router.post("/api/serie/gravar")
def gravar_serie(serie: SeriePayload):
    conn = get_db_connection()  
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO Serie (sessao_id, exercicio_id, numero_serie, tempo, ponto, peso, equipamento, angulo_coletado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (serie.sessao_id, serie.exercicio_id, serie.numero_serie, serie.tempo,
                  serie.ponto, serie.peso, serie.equipamento, serie.angulo_coletado))
            serie_id = cur.fetchone()["id"]
            conn.commit()
        
        return {
            "message": "Série gravada com sucesso",
            "serie_id": serie_id,
            "sessao_id": serie.sessao_id,
            "exercicio_id": serie.exercicio_id,
            "numero_serie": serie.numero_serie,
            "tempo": serie.tempo,
            "ponto": serie.ponto,
            "peso": serie.peso,
            "equipamento": serie.equipamento,
            "angulo_coletado": serie.angulo_coletado
        }
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        conn.close()