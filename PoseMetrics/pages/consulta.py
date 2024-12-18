import mediapipe as mp
import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import cv2
import numpy as np
import time
import datetime

def pagina_consulta():
    st.markdown(
    """
    <style>
        /* Cor do fundo da sidebar */
        [data-testid="stSidebar"] {
            background-color: #46536225; /* Cor verde */
        }
    </style>
    """,
    unsafe_allow_html=True,
)
    
    

    with st.sidebar:
        st.logo("posemetrics_logo.png", size="large", link=None, icon_image=None)
        selected = option_menu(
            menu_title = None,
            options = ["Home", "Indicadores", "Exercícios", "Pacientes", "Consulta", "Relatórios", "Configurações", "Contato", "Sobre"],
            icons=['house', 'graph-up-arrow', 'heart-pulse', 'people', 'calendar2-heart', 'bar-chart', 'gear', 'github', 'question-circle'], 
            styles={
            "container": {"background-color": "#4E937A60"},  
            "icon": {"color": "#A22C29", "font-size": "20px"},  
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "10px",
                "--hover-color": "#A22C2960",
            },
            "nav-link-selected": {"background-color": "#4E937A90", "color": "white"},
        },
        )

    if selected == "Home":
        st.session_state.pagina_atual = "home"  
        st.rerun()
    if selected == "Indicadores":
        st.session_state.pagina_atual = "indicadores"  
        st.rerun()
    if selected == "Exercícios":
        st.session_state.pagina_atual = "exercicios"  
        st.rerun()
    if selected == "Pacientes":
        st.session_state.pagina_atual = "pacientes"  
        st.rerun()
    if selected == "Consulta":
        pass
    if selected == "Relatórios":
        st.session_state.pagina_atual = "relatorios"  
        st.rerun()
    if selected == "Configurações":
        st.session_state.pagina_atual = "configuracoes"  
        st.rerun()
    if selected == "Contato":
        st.session_state.pagina_atual = "contato"
        st.rerun()
    if selected == "Sobre":
        st.session_state.pagina_atual = "sobre"
        st.rerun()




    profissional_email = st.session_state.get("email_profissional", None)

    if not profissional_email:
        profissional_email = "vinivini@gmail.com"
        # st.error("Você precisa estar logado como profissional.")
        # return

    response_profissional = requests.get(
        f"http://127.0.0.1:8000/home/{profissional_email}"
    )

    if response_profissional.status_code == 200:
        profissional = response_profissional.json()
        nome_profissional = profissional["nome_completo"]
        # foto_profissional = profissional["foto"]
        foto_profissional = "https://via.placeholder.com/50"
        

        # st.image(foto_profissional, width=100)
        st.write(f"{nome_profissional}, escolha um paciente para iniciar uma consulta, altere as informações se necessário e inicie uma sessão para coletar dados do paciente.")
    else:
        st.error("Erro ao carregar as informações do profissional.")
        return
    
    col_pacientes, col_altura, col_massa = st.columns([0.6, 0.2, 0.2])

    with col_pacientes:

        response_pacientes = requests.get(
            f"http://127.0.0.1:8000/home/{profissional_email}/listar_pacientes"
        )

        if response_pacientes.status_code == 200:
            pacientes = response_pacientes.json()
            if pacientes:
                df_pacientes = pd.DataFrame(pacientes)
                
                paciente_nome = st.selectbox("Selecione um paciente", df_pacientes['nome'])

                paciente_selecionado = df_pacientes[df_pacientes['nome'] == paciente_nome]
                paciente_id = paciente_selecionado.iloc[0]['id']

                response_sessoes = requests.get(
                    f"http://127.0.0.1:8000/home/pacientes/{paciente_id}/sessoes"
                )

                if response_sessoes.status_code == 200:
                    sessoes = response_sessoes.json()

                    if isinstance(sessoes, list) and sessoes:
                        ultima_sessao = sessoes[-1]
                        ultima_massa = ultima_sessao.get('massa')
                        ultima_altura = ultima_sessao.get('altura')
                        
                        st.info(f"Últimos dados encontrados para {paciente_nome} -> Altura: {ultima_altura} cm, Massa: {ultima_massa} kg")
                    else:
                        st.warning(f"Nenhuma sessão encontrada para {paciente_nome}. Preencha os dados abaixo.")
                else:
                    st.error(f"Erro ao buscar sessões para {paciente_nome}.")
                        
            else:
                st.write("Não há pacientes agendados para este profissional.")
        else:
            st.error("Erro ao carregar a lista de pacientes.")
    
    with col_altura:
        altura = st.number_input(
            "Altura atual (em cm):", 
            value=float(ultima_altura) if 'ultima_altura' in locals() and ultima_altura else 0.0,
            min_value=0.0, 
            step=0.1, 
            format="%.2f"
        )

    with col_massa:
        massa = st.number_input(
            "Peso atual (em kg):", 
            value=float(ultima_massa) if 'ultima_massa' in locals() and ultima_massa else 0.0,
            min_value=0.0, 
            step=0.1, 
            format="%.2f"
        )
    
    

    # st.subheader("Monitoramento de Exercício")
    if 'mostrar_equipamento' not in st.session_state:
        st.session_state.mostrar_equipamento = False

    col6, col7, col8 = st.columns([0.33, 0.33, 0.34])

    with col6:
        start_button = st.button("Iniciar sessão")

    with col7:
        stop_button = st.button("Concluir sessão")

    with col8:
        cancel_button = st.button("Cancelar sessão")

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    if 'running' not in st.session_state:
        st.session_state.running = False
        
    if "serie_table" not in st.session_state:
        st.session_state.serie_table = pd.DataFrame(columns=[
            "sessao_id", "exercicio_id", "numero_serie", "tempo", "ponto", "peso", "equipamento", "angulo_coletado"
        ])

    if 'sessao_iniciada' not in st.session_state:
        st.session_state.sessao_iniciada = False

    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

    if 'sessao_id' not in st.session_state:
        st.session_state.sessao_id = None    

    if start_button:
        payload = {
            "paciente_id": int(paciente_id), 
            "massa": float(massa),  
            "altura": float(altura),  
        }
        
        response_sessao = requests.post(
            "http://127.0.0.1:8000/home/sessoes/iniciar",
            json=payload
        )

        if response_sessao.status_code == 200:
            st.session_state.sessao_id = response_sessao.json()["sessao_id"]
            st.session_state.sessao_iniciada = True
            st.session_state.start_time = time.time()
            st.success(response_sessao.json()["message"])

            st.write("Sessão em andamento. Adicione suas observações abaixo:")

            comentario = st.text_area(
                "Comentários sobre a sessão:",
                placeholder="Digite observações relevantes...",
                key="comentario_sessao"
            )

            
        else:
            st.error("Erro ao iniciar ou atualizar a sessão.")

        st.session_state.mostrar_equipamento = True
        st.session_state.numero_serie = 1



    if stop_button:
        if st.session_state.get("sessao_iniciada", False):
            if st.session_state.start_time is not None:
                tempo_fim = time.time()
                tempo_total = (tempo_fim - st.session_state.start_time) / 60  # Tempo total em minutos
                
                comentario = st.session_state.get("comentario_sessao", "")

                payload_concluir = {
                    "sessao_id": st.session_state.sessao_id,
                    "tempo_total": round(tempo_total, 2),  
                    "observacoes": comentario
                }

                response_concluir = requests.put(
                    "http://127.0.0.1:8000/home/sessoes/concluir",
                    json=payload_concluir
                )

                if response_concluir.status_code == 200:
                    st.success("Sessão concluída com sucesso!")
                else:
                    st.error("Erro ao concluir a sessão.")

                st.session_state.sessao_iniciada = False
                st.session_state.start_time = None
                st.session_state.sessao_id = None
                st.session_state.mostrar_equipamento = False
                st.session_state.running = False
            else:
                st.error("Dados da sessão não registrados corretamente.")
        else:
            st.warning("Inicie uma sessão antes de concluí-la.")


    if cancel_button:
        cancela_sessao()
        st.session_state.mostrar_equipamento = False
        st.session_state.running = False

    if st.session_state.mostrar_equipamento:

        col_exercicios, col_equipamento, col_peso = st.columns([0.6, 0.2, 0.2])

        with col_exercicios:
            response_exercicios = requests.get(f"http://127.0.0.1:8000/home/{profissional_email}/exercicios")
            if response_exercicios.status_code == 200:
                exercicios = response_exercicios.json()
                exercicio_selecionado = st.selectbox("Selecione o exercício", [e['nome'] for e in exercicios])

                dados_exercicio = next(e for e in exercicios if e['nome'] == exercicio_selecionado)

                ponto1, ponto2, ponto3 = dados_exercicio['x1'], dados_exercicio['x2'], dados_exercicio['x3']
                angulo_minimo = dados_exercicio['angulo_minimo_exercicio']
                angulo_maximo = dados_exercicio['angulo_maximo_exercicio']
                st.session_state.exercicio_id = dados_exercicio['id']
            else:
                st.error("Erro ao carregar a lista de exercícios.")
                return

        with col_equipamento:
            opcoes = ["Halter", "Elástico", "Barra", "Polia", "Peso do Corpo"]
            equip = st.selectbox("Escolha um equipamento", opcoes)
            st.session_state.equipamento = equip

        with col_peso:
            peso = st.number_input("Peso (em kg):", min_value=0.0, step=0.1, format="%.2f")
            st.session_state.peso_coletado = peso

        
        col9, col10, col11 = st.columns([0.33, 0.33, 0.34])

        with col9:
            start_serie_button = st.button("Iniciar Série")
            
        with col10:
            cancel_serie_button = st.button("Cancelar Série")
            
        with col11:
            save_serie_button = st.button("Gravar Série")

        if start_serie_button:
            st.write("Série iniciada!")
            st.session_state.running = True
            st.session_state.data_table = None
        if cancel_serie_button:
            st.write("Série cancelada!")
            st.session_state.running = False  
        
        if save_serie_button:
            st.write("Série gravada!")
            for index, row in st.session_state.data_table.iterrows():
                tempo = row["Tempo (s)"]
                ponto = row["Posição"]
                angulo = row["Ângulo (graus)"]
                
                gravar_serie(
                    sessao_id=st.session_state.sessao_id,
                    exercicio_id=st.session_state.exercicio_id,  
                    numero_serie=st.session_state.numero_serie,
                    tempo=tempo,
                    ponto=ponto,
                    peso=st.session_state.peso_coletado,
                    equipamento=st.session_state.equipamento,
                    angulo_coletado=round(angulo, 1)
                )
                
            st.session_state.numero_serie += 1 
            st.write("Tabela de Séries Gravadas:")
            st.table(st.session_state.serie_table) 
            st.session_state.serie_table = None

        


        if "data_table" not in st.session_state:
            st.session_state.data_table = pd.DataFrame(columns=["Tempo (s)", "Posição", "Ângulo (graus)"])
            st.session_state.start_time = None  
            

    if st.session_state.running:

        cap = cv2.VideoCapture(0)
        counter = 0 
        stage = None
        col_video, col_tabela = st.columns([0.7, 0.3])

        with col_video:
            video_placeholder = st.empty()
            stage_text = st.empty()

            if st.button("Gravar"):
                current_time = time.time()

                if st.session_state.start_time is None:
                    st.session_state.start_time = current_time

                elapsed_time = round(current_time - st.session_state.start_time, 2)
                posicao = st.session_state.ponto  
                angulo = st.session_state.angle 

                gravar_dados(elapsed_time, posicao, angulo)

        with col_tabela:
            st.table(st.session_state.data_table)

        st.write("") #gambiarra de alto nível para não gerar frozen frame kkkkk - não retirar, sujeita a paulada

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened() and st.session_state.running:
                ret, frame = cap.read()

                if not ret:
                    st.write("Erro ao capturar vídeo.")
                    break

                frame = resize_frame(frame, 640, 480)

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark

                    ponto1_coords = [landmarks[ponto1].x, landmarks[ponto1].y]
                    ponto2_coords = [landmarks[ponto2].x, landmarks[ponto2].y]
                    ponto3_coords = [landmarks[ponto3].x, landmarks[ponto3].y]
                    
                    st.session_state.angle = calculate_angle(ponto1_coords, ponto2_coords, ponto3_coords)

                    cv2.putText(image, f"Angulo: {int(st.session_state.angle)}", 
                                (int(ponto2_coords[0] * frame.shape[1]), int(ponto2_coords[1] * frame.shape[0] - 20)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
 
                    if st.session_state.angle >= angulo_maximo:
                        stage = "baixo"
                        st.session_state.ponto = stage
                    if st.session_state.angle <= angulo_minimo and stage == 'baixo':
                        stage = "cima"
                        st.session_state.ponto = stage
                        counter += 1

                    if "aviso_exibido" not in st.session_state:
                        st.session_state.aviso_exibido = False

                    if dados_exercicio['tipo'] == 'Flexibilidade':
                        if st.session_state.angle > angulo_maximo and not st.session_state.aviso_exibido:
                            st.success(f"Você ultrapassou o ângulo máximo do exercício ({angulo_maximo}°)!")
                            st.session_state.aviso_exibido = True  
                        elif st.session_state.angle < angulo_minimo and not st.session_state.aviso_exibido:
                            st.success(f"Você ultrapassou o ângulo mínimo do exercício ({angulo_minimo}°)!")
                            st.session_state.aviso_exibido = True  
                        elif st.session_state.angle >= angulo_minimo and st.session_state.angle <= angulo_maximo:
                            st.session_state.aviso_exibido = False  

                    stage_text.write(f'Estágio: {stage}')

                except Exception as e:
                    # st.write("Erro:", e)
                    pass

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                video_placeholder.image(image, channels="BGR", width = 800)

                time.sleep(0.1)

        cap.release()
    else:
        st.write("Pressione 'Iniciar sessão' para começar.")



def calculate_angle(a, b, c):
    a = np.array(a) 
    b = np.array(b)  
    c = np.array(c)  

    rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(rad * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def cancela_sessao():
    pass

def gravar_dados(tempo, posicao, angulo):
    nova_linha = {"Tempo (s)": tempo, "Posição": posicao, "Ângulo (graus)": angulo}
    st.session_state.data_table = pd.concat([st.session_state.data_table, pd.DataFrame([nova_linha])], ignore_index=True)


def gravar_serie(sessao_id, exercicio_id, numero_serie, tempo, ponto, peso, equipamento, angulo_coletado):
    nova_linha = {
        "sessao_id": sessao_id,
        "exercicio_id": exercicio_id,
        "numero_serie": numero_serie,
        "tempo": tempo,
        "ponto": ponto,
        "peso": peso,
        "equipamento": equipamento,
        "angulo_coletado": angulo_coletado
    }
    url_api = "http://127.0.0.1:8000/home/api/serie/gravar" 
    response = requests.post(url_api, json=nova_linha)

    if response.status_code == 200:
        # st.success("Série gravada com sucesso!")
        pass
    else:
        st.error("Erro ao gravar a série na API.")

    nova_linha_df = pd.DataFrame([nova_linha])  
    st.session_state.serie_table = pd.concat([st.session_state.serie_table, nova_linha_df], ignore_index=True)  
