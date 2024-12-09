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
            # Obter o ID do paciente selecionado
                paciente_selecionado = df_pacientes[df_pacientes['nome'] == paciente_nome]
                paciente_id = paciente_selecionado.iloc[0]['id']

                # Buscar as sessões do paciente
                response_sessoes = requests.get(
                    f"http://127.0.0.1:8000/home/pacientes/{paciente_id}/sessoes"
                )

                if response_sessoes.status_code == 200:
                    sessoes = response_sessoes.json()

                    if isinstance(sessoes, list) and sessoes:
                        # Última sessão
                        ultima_sessao = sessoes[-1]
                        ultima_massa = ultima_sessao.get('massa')
                        ultima_altura = ultima_sessao.get('altura')
                        
                        st.info(f"Últimos dados encontrados para {paciente_nome}:")
                        st.write(f"Altura: {ultima_altura} cm, Massa: {ultima_massa} kg")
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
    
    

    st.subheader("Monitoramento de Exercício")
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
        
    # Definir as variáveis de configuração e tabelas
    if "serie_table" not in st.session_state:
        st.session_state.serie_table = pd.DataFrame(columns=[
            "sessao_id", "exercicio_id", "numero_serie", "tempo", "ponto", "peso", "equipamento", "angulo_coletado"
        ])
        # st.session_state.numero_serie = 1  # Iniciar o contador de séries
    # Inicialização de variáveis de estado
    if 'sessao_iniciada' not in st.session_state:
        st.session_state.sessao_iniciada = False

    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

    if 'sessao_id' not in st.session_state:
        st.session_state.sessao_id = None    

    if start_button:
        # Preparar os dados para a requisição
        payload = {
            "paciente_id": int(paciente_id),  # Garantir que o id seja do tipo int
            "massa": float(massa),  # Garantir que a massa seja do tipo float
            "altura": float(altura),  # Garantir que a altura seja do tipo float
        }
        
        # Verificar ou criar/atualizar a sessão
        response_sessao = requests.post(
            "http://127.0.0.1:8000/home/sessoes/iniciar",
            json=payload
        )

        if response_sessao.status_code == 200:
            st.session_state.sessao_id = response_sessao.json()["sessao_id"]
            st.session_state.sessao_iniciada = True
            st.session_state.start_time = time.time()
            # st.session_state.running = True
            st.success(response_sessao.json()["message"])

            # Iniciar o temporizador
            # st.session_state.start_time = time.time()
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
            # Verificar se o start_time foi corretamente inicializado
            if st.session_state.start_time is not None:
                # Calcular o tempo total da sessão
                tempo_fim = time.time()
                tempo_total = (tempo_fim - st.session_state.start_time) / 60  # Tempo total em minutos
                
            # Pegar o comentário já preenchido
                comentario = st.session_state.get("comentario_sessao", "")

                # Preparar o payload para a requisição de conclusão
                payload_concluir = {
                    "sessao_id": st.session_state.sessao_id,
                    "tempo_total": round(tempo_total, 2),  # Arredondar para 2 casas decimais
                    "observacoes": comentario
                }
                # st.write(payload_concluir)

                # Enviar os dados para o backend
                response_concluir = requests.put(
                    "http://127.0.0.1:8000/home/sessoes/concluir",
                    json=payload_concluir
                )

                if response_concluir.status_code == 200:
                    st.success("Sessão concluída com sucesso!")
                else:
                    st.error("Erro ao concluir a sessão.")

                # Resetar estado da sessão
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
        st.subheader("Configuração do Equipamento")

        col_exercicios, col_equipamento, col_peso = st.columns([0.6, 0.2, 0.2])

        with col_exercicios:
            response_exercicios = requests.get(f"http://127.0.0.1:8000/home/{profissional_email}/exercicios")
            if response_exercicios.status_code == 200:
                exercicios = response_exercicios.json()
                exercicio_selecionado = st.selectbox("Selecione o exercício", [e['nome'] for e in exercicios])

                # Obter os dados do exercício selecionado
                dados_exercicio = next(e for e in exercicios if e['nome'] == exercicio_selecionado)

                # Extrair os índices dos pontos e limites de ângulo
                ponto1, ponto2, ponto3 = dados_exercicio['x1'], dados_exercicio['x2'], dados_exercicio['x3']
                angulo_minimo = dados_exercicio['angulo_minimo_exercicio']
                angulo_maximo = dados_exercicio['angulo_maximo_exercicio']
                st.session_state.exercicio_id = dados_exercicio['id']
            else:
                st.error("Erro ao carregar a lista de exercícios.")
                return

        with col_equipamento:
            opcoes = ["Halter", "Elástico", "Barra", "Polia"]
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
            # start_time = None
            # serie_data = []  # Substituir pela lógica da série
        if cancel_serie_button:
            st.write("Série cancelada!")
            st.session_state.running = False  # Substituir pela lógica de cancelamento

        
        if save_serie_button:
            st.write("Série gravada!")
            # Passar os dados da tabela 'data_table' para a tabela 'serie'
            for index, row in st.session_state.data_table.iterrows():
                tempo = row["Tempo (s)"]
                ponto = row["Posição"]
                angulo = row["Ângulo (graus)"]
                
                # Supondo que peso e equipamento sejam inseridos pelo profissional
                # peso_coletado = st.session_state.get("peso", 0)  # Valor do peso
                # equipamento = st.session_state.get("equip", "")  # Equipamento selecionado
                
                # Chamar a função para gravar os dados na tabela 'serie'
                gravar_serie(
                    sessao_id=st.session_state.sessao_id,
                    exercicio_id=st.session_state.exercicio_id,  # Você deve garantir que o exercicio_id esteja disponível
                    numero_serie=st.session_state.numero_serie,
                    tempo=tempo,
                    ponto=ponto,
                    peso=st.session_state.peso_coletado,
                    equipamento=st.session_state.equipamento,
                    angulo_coletado=round(angulo, 1)
                )
                
            st.session_state.numero_serie += 1 
            # Exibir a tabela de séries
            st.write("Tabela de Séries Gravadas:")
            st.table(st.session_state.serie_table)  # Substituir pela lógica de gravação
            st.session_state.serie_table = None

        


        if "data_table" not in st.session_state:
            st.session_state.data_table = pd.DataFrame(columns=["Tempo (s)", "Posição", "Ângulo (graus)"])
            st.session_state.start_time = None  # Para rastrear o tempo inicial

            

    if st.session_state.running:

        cap = cv2.VideoCapture(0)
        counter = 0 
        stage = None
                # Divisão de colunas: 80% para o vídeo e 20% para a tabela
        col_video, col_tabela = st.columns([0.7, 0.3])

        with col_video:
            video_placeholder = st.empty()
            # rep_counter = st.empty()
            stage_text = st.empty()

            if st.button("Gravar"):
            # Gravar o tempo atual, posição e ângulo
                current_time = time.time()

                if st.session_state.start_time is None:
                    st.session_state.start_time = current_time

                elapsed_time = round(current_time - st.session_state.start_time, 2)
                posicao = st.session_state.ponto  # Usar a variável 'stage' para posição (Cima, Baixo)
                angulo = st.session_state.angle # Substituir com a lógica real de cálculo do ângulo

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

                # Recolorir imagem para RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark

                    # Obter coordenadas dos pontos do exercício selecionado
                    ponto1_coords = [landmarks[ponto1].x, landmarks[ponto1].y]
                    ponto2_coords = [landmarks[ponto2].x, landmarks[ponto2].y]
                    ponto3_coords = [landmarks[ponto3].x, landmarks[ponto3].y]
                    
                    # Calcular o ângulo entre os pontos
                    st.session_state.angle = calculate_angle(ponto1_coords, ponto2_coords, ponto3_coords)

                    # Exibir ângulo na imagem
                    cv2.putText(image, f"Angulo: {int(st.session_state.angle)}", 
                                (int(ponto2_coords[0] * frame.shape[1]), int(ponto2_coords[1] * frame.shape[0] - 20)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
                    # Lógica de contagem das repetições com base nos limites definidos
                    # st.session_state.ponto = ""
                    if st.session_state.angle >= angulo_maximo:
                        stage = "baixo"
                        st.session_state.ponto = stage
                    if st.session_state.angle <= angulo_minimo and stage == 'baixo':
                        stage = "cima"
                        st.session_state.ponto = stage
                        counter += 1

                    # Atualizar contadores na interface
                    # rep_counter.write(f'Contagem: {counter}')
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

# Função para adicionar uma nova linha à tabela
def gravar_dados(tempo, posicao, angulo):
    nova_linha = {"Tempo (s)": tempo, "Posição": posicao, "Ângulo (graus)": angulo}
    st.session_state.data_table = pd.concat([st.session_state.data_table, pd.DataFrame([nova_linha])], ignore_index=True)


# Função para gravar os dados da série na tabela e enviar para a API
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
    st.write(nova_linha)
    # Enviar os dados para a API (substitua com sua URL real)
    url_api = "http://127.0.0.1:8000/home/api/serie/gravar"  # A URL para a rota que grava os dados
    response = requests.post(url_api, json=nova_linha)

    if response.status_code == 200:
        st.success("Série gravada com sucesso!")
    else:
        st.error("Erro ao gravar a série na API.")

    nova_linha_df = pd.DataFrame([nova_linha])  # Converter nova_linha em DataFrame
    st.session_state.serie_table = pd.concat([st.session_state.serie_table, nova_linha_df], ignore_index=True)  # Usar pd.concat para adicionar nova linha
    # st.session_state.numero_serie += 1  # Incrementar o número da série