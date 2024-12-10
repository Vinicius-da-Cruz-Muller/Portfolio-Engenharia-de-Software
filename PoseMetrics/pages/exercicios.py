import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser


def exibir_exercicios():
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
        pass
    if selected == "Pacientes":
        st.session_state.pagina_atual = "pacientes"  
        st.rerun()
    if selected == "Consulta":
        st.session_state.pagina_atual = "consulta"  
        st.rerun()
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
            st.header(f"Bem-vindo, {nome_profissional}!")
        else:
            st.error("Erro ao carregar as informações do profissional.")
            return

    
        
        st.title("Gerenciar Exercícios")
        
        with st.expander("Listar Exercícios", expanded=False):
            st.subheader("Exercícios Cadastrados")
            response_exercicios = requests.get("http://127.0.0.1:8000/home/{profissional_email}/exercicios")
            if response_exercicios.status_code == 200:
                exercicios = response_exercicios.json()
                df_exercicios = pd.DataFrame(exercicios)
                st.dataframe(df_exercicios)


        with st.expander("Editar Exercício", expanded=False):
            st.subheader("Exercícios Cadastrados")
            response_exercicios = requests.get("http://127.0.0.1:8000/home/{profissional_email}/exercicios")
            if response_exercicios.status_code == 200:
                exercicios = response_exercicios.json()
                df_exercicios = pd.DataFrame(exercicios)

                exercicio_selecionado = st.selectbox("Selecione um exercício para editar:", df_exercicios["nome"])
                if exercicio_selecionado:
                    exercicio = df_exercicios[df_exercicios["nome"] == exercicio_selecionado].iloc[0]

                    with st.form(key="editar_exercicio"):
                        nome_edit = st.text_input("Nome do exercício:", exercicio["nome"])
                        grupo_muscular_edit = st.text_input("Grupo muscular:", exercicio["grupo_muscular"])
                        lado_edit = st.selectbox("Lado:", ["Esquerdo", "Direito", "Ambos"], index=["Esquerdo", "Direito", "Ambos"].index(exercicio["lado"]))
                        angulo_minimo_edit = st.number_input(
                            "Ângulo Mínimo:",
                            min_value=0,
                            max_value=180,
                            step=1,
                            value=int(exercicio["angulo_minimo_exercicio"]) 
                        )

                        angulo_maximo_edit = st.number_input(
                            "Ângulo Máximo:",
                            min_value=0,
                            max_value=180,
                            step=1,
                            value=int(exercicio["angulo_maximo_exercicio"])  
                        )

                        x1_edit = st.number_input(
                            "Ponto X1 (Mediapipe):",
                            min_value=0,
                            step=1,
                            value=int(exercicio["x1"])  
                        )

                        x2_edit = st.number_input(
                            "Ponto X2 (Mediapipe):",
                            min_value=0,
                            step=1,
                            value=int(exercicio["x2"])  
                        )

                        x3_edit = st.number_input(
                            "Ponto X3 (Mediapipe):",
                            min_value=0,
                            step=1,
                            value=int(exercicio["x3"])  
                        )
                        descricao_edit = st.text_area("Descrição do exercício:", exercicio["descricao"])
                        tipo_opcoes = ["Força", "Flexibilidade", "Resistência", "Outro"]

                        tipo_edit = st.selectbox(
                            "Tipo:",
                            tipo_opcoes,
                            index=tipo_opcoes.index(exercicio["tipo"]) if exercicio["tipo"] in tipo_opcoes else 3  
                        )
                        submit_editar = st.form_submit_button("Salvar Alterações")

                        if submit_editar:
                            exercicio_editado = {
                                "nome": nome_edit,
                                "grupo_muscular": grupo_muscular_edit,
                                "lado": lado_edit,
                                "x1": x1_edit,
                                "x2": x2_edit,
                                "x3": x3_edit,
                                "angulo_minimo_exercicio": angulo_minimo_edit,
                                "angulo_maximo_exercicio": angulo_maximo_edit,
                                "descricao": descricao_edit,
                                "tipo": tipo_edit
                            }
                            exercicio_id = exercicio["id"]
                            response_edit = requests.put(f"http://127.0.0.1:8000/home/{profissional_email}/exercicios/{exercicio_id}", json=exercicio_editado)
                            if response_edit.status_code == 200:
                                st.success("Exercício atualizado com sucesso!")
                            else:
                                st.error("Erro ao atualizar exercício.")
            else:
                st.error("Erro ao carregar lista de exercícios.")

        with st.expander("Adicionar Exercício", expanded=False):
            st.subheader("Adicionar Novo Exercício")
            with st.form(key="adicionar_exercicio"):
                nome = st.text_input("Nome do exercício:")
                grupo_muscular = st.text_input("Grupo muscular:")
                lado = st.selectbox("Lado:", ["Esquerdo", "Direito", "Ambos"])
                x1 = st.number_input("Ponto X1 (Mediapipe):", min_value=0, step=1)
                x2 = st.number_input("Ponto X2 (Mediapipe):", min_value=0, step=1)
                x3 = st.number_input("Ponto X3 (Mediapipe):", min_value=0, step=1)
                angulo_minimo = st.number_input("Ângulo Mínimo:", min_value=0, max_value=180, step=1)
                angulo_maximo = st.number_input("Ângulo Máximo:", min_value=0, max_value=180, step=1)
                descricao = st.text_area("Descrição do exercício:")
                tipo = st.selectbox("Tipo:", ["Força", "Flexibilidade", "Resistência", "Outro"])

                submit_adicionar = st.form_submit_button("Adicionar")

                if submit_adicionar:
                    novo_exercicio = {
                        "nome": nome,
                        "grupo_muscular": grupo_muscular,
                        "lado": lado,
                        "x1": x1,
                        "x2": x2,
                        "x3": x3,
                        "angulo_minimo_exercicio": angulo_minimo,
                        "angulo_maximo_exercicio": angulo_maximo,
                        "descricao": descricao,
                        "tipo": tipo
                    }
                    response = requests.post(f"http://127.0.0.1:8000/home/{profissional_email}/exercicios/criar_exercicio", json=novo_exercicio)
                    if response.status_code == 200:
                        st.success("Exercício adicionado com sucesso!")
                    else:
                        st.error("Erro ao adicionar exercício.")
            
    
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

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <h3 style="text-align: left; margin-bottom: 20px;">Índice de Pontos</h3>
            """,
            unsafe_allow_html=True,
        )
        
        st.image("pose_landmarks_index.png", use_container_width=True)
        st.write("Utilize o índice de pontos para entender o correto acompanhamento do movimento do paciente.")
        st.write("O PoseMetrics se baseia em uma lógica de três pontos para calcular os ângulos dos membros aferidos e utilizar os dados coletados nas análises do paciente. Não utilize pontos muito afastados ou que não pertençam ao mesmo grupo muscular, pois isso pode afetar a acurácia da análise visual.")

        st.markdown(
    """
    <style>
        /* Estilo do footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #4E937A70;
            color: white;
            text-align: center;
            padding: 5px;
            font-size: 14px;
        }
    </style>
    <div class="footer">
        PoseMetrics © 2024 - Todos os direitos reservados
    </div>
    """,
    unsafe_allow_html=True,
)