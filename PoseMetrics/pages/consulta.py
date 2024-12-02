import mediapipe as mp
import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import cv2
import numpy as np
import time

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
            # menu_icon="menu-button-wide-fill", 
            # default_index=0
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
    # if selected == "Sobre":
    #     github_url = "https://github.com/Vinicius-da-Cruz-Muller"  # Substitua pelo link do seu GitHub
    #     webbrowser.open_new_tab(github_url)

    col1, col2 = st.columns([0.8, 0.2])

    
    with col1:

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
            st.write(f"{nome_profissional}, escolha um paciente para iniciar uma consulta.")
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
            #         paciente_id = df_pacientes["id"]
                    
            #         # paciente_selecionado = df_pacientes[df_pacientes['nome'] == paciente_nome].iloc[0]
            #         # editar_paciente(paciente_selecionado)
                        
                else:
                    st.write("Não há pacientes agendados para este profissional.")
            else:
                st.error("Erro ao carregar a lista de pacientes.")
        
        with col_altura:
            altura = st.number_input("Altura atual (em cm):", min_value=0.0, step=0.1, format="%.2f")
        
        with col_massa:
            massa = st.number_input("Peso atual (em kg):", min_value=0.0, step=0.1, format="%.2f")

        
        col_exercicios, col_equipamento, col_peso = st.columns([0.6, 0.2, 0.2])
        with col_exercicios:
            response_exercicios = requests.get(f"http://127.0.0.1:8000/home/{profissional_email}/exercicios")
            if response_exercicios.status_code == 200:
                exercicios = response_exercicios.json()
                exercicio_selecionado = st.selectbox("Selecione o exercício", [e['nome'] for e in exercicios])
            else:
                st.error("Erro ao carregar a lista de exercícios.")
                return
            
        with col_equipamento:
            opcoes = ["Halter", "Elástico", "Barra", "Polia"]

            equip = st.selectbox("Escolha um equipamento", opcoes)

        with col_peso:
            peso = st.number_input("Peso (em kg):", min_value=0.0, step=0.1, format="%.2f")

        
        

        # Obter o ID do paciente da sessão
        # paciente_id = st.session_state.get("paciente_id", None)

        # if paciente_id is None:
        #     st.error("Nenhum paciente selecionado. Por favor, volte e selecione um paciente.")
        #     return

        # # Carregar informações do paciente
        # response = requests.get(f"http://127.0.0.1:8000/home/paciente/{paciente_id}")
        # if response.status_code == 200:
        #     paciente = response.json()
        #     st.subheader(f"Paciente: {paciente['nome']}")
        # else:
        #     print(paciente_id)
        #     st.error("Erro ao carregar as informações do paciente.")
        #     return

        # Exibir informações adicionais
        # st.markdown("**Sessão em andamento...**")
        

        st.subheader("Monitoramento de Exercício")

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

        if start_button:
            st.session_state.running = True

        if stop_button:
            st.session_state.running = False

        if cancel_button:
            cancela_sessao()

        if st.session_state.running:
            cap = cv2.VideoCapture(0)

            counter = 0 
            stage = None

            video_placeholder = st.empty()

            rep_counter = st.empty()
            stage_text = st.empty()

            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                while cap.isOpened() and st.session_state.running:
                    ret, frame = cap.read()

                    if not ret:
                        st.write("Erro ao capturar vídeo.")
                        break

                    frame = resize_frame(frame, 640, 480)

                    # Recolorir imagem para RGB
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False

                    results = pose.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    try:
                        landmarks = results.pose_landmarks.landmark
                        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                        angle = calculate_angle(shoulder, elbow, wrist)

                        # Lógica de contagem das repetições
                        if angle > 80:
                            stage = "baixo"
                        if angle < 30 and stage == 'baixo':
                            stage = "cima"
                            counter += 1

                        rep_counter.write(f'Contagem: {counter}')
                        stage_text.write(f'Estágio: {stage}')

                    except Exception as e:
                        st.write("Erro:", e)

                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                    video_placeholder.image(image, channels="BGR", use_container_width=True)

                    time.sleep(0.1)

            cap.release()
        else:
            st.write("Pressione 'Iniciar Captura' para começar.")

    with col2:
        st.markdown(
            f"""
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px;">
                <div style="display: flex; align-items: center; justify-content: flex-end;">
                    <p style="font-size:18px; margin: 0; padding-right: 10px;">{nome_profissional}</p>
                    <img src="{foto_profissional}" style="border-radius:50%; width:50px; height:50px;">
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# def encerrar_sessao():
#     # Função para encerrar a sessão
#     st.session_state.pagina_atual = "usuarios"
#     st.rerun()


def calculate_angle(a, b, c):
    a = np.array(a)  # primeiro ponto
    b = np.array(b)  # segundo ponto
    c = np.array(c)  # terceiro ponto

    rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(rad * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

    # Função para redimensionar frames
def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def cancela_sessao():
    pass