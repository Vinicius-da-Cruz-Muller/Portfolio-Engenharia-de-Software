import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time

# Função para calcular ângulo
def calculate_angle(a, b, c):
    a = np.array(a)  # primeiro ponto
    b = np.array(b)  # segundo ponto
    c = np.array(c)  # terceiro ponto

    rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(rad * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Inicialize o Streamlit
st.title("Monitoramento de Exercício")
st.sidebar.header("Configurações")
start_button = st.sidebar.button("Iniciar Captura")
stop_button = st.sidebar.button("Parar Captura")

# Inicializa o MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Variáveis de estado para controle de captura
if 'running' not in st.session_state:
    st.session_state.running = False

if start_button:
    st.session_state.running = True

if stop_button:
    st.session_state.running = False

if st.session_state.running:
    cap = cv2.VideoCapture(0)

    # Variáveis de contagem de repetições
    counter = 0 
    stage = None

    # Inicializa o Streamlit com placeholder para o vídeo
    video_placeholder = st.empty()

    # Adiciona contadores e estágio
    rep_counter = st.empty()
    stage_text = st.empty()

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and st.session_state.running:
            ret, frame = cap.read()

            if not ret:
                st.write("Erro ao capturar vídeo.")
                break

            # Recolorir imagem para RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Realizar a detecção
            results = pose.process(image)

            # Recolorir de volta para BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extraindo landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Calcular ângulo
                angle = calculate_angle(shoulder, elbow, wrist)

                # Lógica de contagem de repetições
                if angle > 160:
                    stage = "down"
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1

                # Atualizar as informações no Streamlit
                rep_counter.write(f'Contagem: {counter}')
                stage_text.write(f'Estágio: {stage}')

            except Exception as e:
                st.write("Erro:", e)

            # Desenhar as landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Renderizar o vídeo no Streamlit
            video_placeholder.image(image, channels="BGR", use_column_width=True)

            # Adicionar um delay se necessário
            time.sleep(0.1)

    cap.release()
else:
    st.write("Pressione 'Iniciar Captura' para começar.")
