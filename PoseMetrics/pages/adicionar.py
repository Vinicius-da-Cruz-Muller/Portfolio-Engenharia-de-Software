import streamlit as st
import requests
from streamlit_option_menu import option_menu
import time


# Função para adicionar um novo paciente
def adicionar_novo_paciente():
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
        st.session_state.pagina_atual = "pacientes"  
        st.rerun()
    if selected == "Indicadores":
        st.session_state.pagina_atual = "indicadores"  
        st.rerun()
    if selected == "Exercícios":
        st.session_state.pagina_atual = "exercicios"  
        st.rerun()
    if selected == "Pacientes":
        pass
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
            foto_profissional = "https://via.placeholder.com/50"
        else:
            st.error("Erro ao carregar as informações do profissional.")
            return
        
        st.title("Adicionar Novo Paciente")  # Título da página
        
        with st.form("my_form"):  # Formulário para inserção dos dados
            nome = st.text_input("Nome")
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")
            estado_civil = st.text_input("Estado Civil")
            data_nascimento = st.date_input("Data de Nascimento")
            endereco = st.text_input("Endereço")
            condicao = st.text_input("Condição do Paciente")
            inicio_tratamento = st.date_input("Início do Tratamento")
            fim_tratamento = st.date_input("Fim do Tratamento")
            prox_sessao = st.date_input("Próxima Sessão")
            hora_prox_sessao = st.text_input("Horário da Próxima Sessão (HH:MM)")
            foto = st.file_uploader("Foto do Paciente", type=["jpg", "jpeg", "png"])
            
            # Botão para enviar o formulário
            submitted = st.form_submit_button("Adicionar Paciente")
            
            if submitted:
                if not nome or not telefone or not email:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
                else:

                    foto_bytes = foto.read() if foto else None
                    # Preparar os dados para enviar
                    paciente_data = {
                        "nome": nome,
                        "telefone": telefone,
                        "email": email,
                        "estado_civil": estado_civil,
                        "data_nascimento": str(data_nascimento),
                        "endereco": endereco,
                        "condicao": condicao,
                        "inicio_tratamento": str(inicio_tratamento),
                        "fim_tratamento": str(fim_tratamento),
                        "prox_sessao": str(prox_sessao),
                        "hora_prox_sessao": hora_prox_sessao,
                        "atendente": profissional_email
                    }
                    
                    files = {"foto": ("foto.jpg", foto_bytes, "image/jpeg")} if foto_bytes else None
                    # Fazer a requisição para a API
                    response = requests.post(
                        f"http://127.0.0.1:8000/home/{profissional_email}/adicionar_paciente",
                        data=paciente_data,
                        files=files,
                    )

                    if response.status_code == 200:
                        st.success("Paciente adicionado com sucesso.")
                        time.sleep(2)
                        st.session_state.pagina_atual = "pacientes"  
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar paciente. Verifique os dados e tente novamente.")



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




# Chamar a função para adicionar paciente
if __name__ == "__main__":
    adicionar_novo_paciente()
