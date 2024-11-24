import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu


def exibir_usuarios():
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
            options = ["Home", "Indicadores", "Usuários", "Relatórios", "Contato", "Sobre"],
            icons=['house', 'graph-up-arrow', 'people', 'bar-chart', 'github', 'question-circle'], 
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
    if selected == "Usuários":
        pass
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

        response_pacientes = requests.get(
            f"http://127.0.0.1:8000/home/{profissional_email}/listar_pacientes"
        )

        if response_pacientes.status_code == 200:
            pacientes = response_pacientes.json()
            if pacientes:
                df_pacientes = pd.DataFrame(pacientes)
                col_select, col_buttons = st.columns([0.8, 0.2])
                with col_select:
                    paciente_nome = st.selectbox("Selecione um paciente", df_pacientes['nome'])

                
                    paciente_selecionado = df_pacientes[df_pacientes['nome'] == paciente_nome].iloc[0]
                    editar_paciente(paciente_selecionado)
                    # st.write(f"Nome: {paciente_selecionado['nome']}")
                    # st.write(f"Status: {paciente_selecionado['status']}")
                    # st.write(f"Endereço: {paciente_selecionado['endereco']}")
                    # st.write(f"Telefone: {paciente_selecionado['telefone']}")
                    # st.write(f"e-mail: {paciente_selecionado['email']}")
                    # st.write(f"Estado civil: {paciente_selecionado['estado_civil']}")
                    # st.write(f"Data de nascimento: {paciente_selecionado['data_nascimento']}")
                    # st.write(f"Condição do paciente: {paciente_selecionado['condicao']}")
                    # st.write(f"Início do tratamento: {paciente_selecionado['inicio_tratamento']}")
                    # st.write(f"Fim do tratamento: {paciente_selecionado['fim_tratamento']}")
                    # st.write(f"Próxima sessão: {paciente_selecionado['prox_sessao']}")
                    # st.write(f"Horário da próxima sessão: {paciente_selecionado['hora_prox_sessao']}")

                with col_buttons:
                        # Botão de editar paciente
                        if st.button("Novo Paciente"):
                            adicionar_novo_paciente()

                        # if st.button("Editar Paciente"):
                        #     editar_paciente(paciente_selecionado)

                        if st.button("Ir para Sessão"):
                            st.session_state.pagina_atual = "sessao"
                            st.session_state.paciente_id = paciente_selecionado['id']  # Salva o ID do paciente
                            st.rerun()
            else:
                st.write("Não há pacientes agendados para este profissional.")
        else:
            st.error("Erro ao carregar a lista de pacientes.")

        


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


def editar_paciente(paciente):
    st.subheader("Dados do Paciente")

    # Inicializar estado de edição
    if "modo_edicao" not in st.session_state:
        st.session_state["modo_edicao"] = False

    if st.session_state["modo_edicao"]:
        # Campos editáveis
        campos = {
            "nome": st.text_input("Nome", paciente.get("nome", "")),
            "telefone": st.text_input("Telefone", paciente.get("telefone", "")),
            "prox_sessao": st.date_input(
                "Próxima Sessão", pd.to_datetime(paciente.get("prox_sessao", pd.Timestamp.now()))
            ),
            "endereco": st.text_input("Endereço", paciente.get("endereco", "")),
            "email": st.text_input("E-mail", paciente.get("email", "")),
            "estado_civil": st.text_input("Estado Civil", paciente.get("estado_civil", "")),
            "data_nascimento": st.date_input(
                "Data de Nascimento", pd.to_datetime(paciente.get("data_nascimento", pd.Timestamp.now()))
            ),
            "condicao": st.text_input("Condição do Paciente", paciente.get("condicao", "")),
            "inicio_tratamento": st.date_input(
                "Início do Tratamento", pd.to_datetime(paciente.get("inicio_tratamento", pd.Timestamp.now()))
            ),
            "fim_tratamento": st.date_input(
                "Fim do Tratamento", pd.to_datetime(paciente.get("fim_tratamento", pd.Timestamp.now()))
            ),
            "hora_prox_sessao": st.text_input(
                "Horário da Próxima Sessão", paciente.get("hora_prox_sessao", "00:00")
            ),
        }

        if st.button("Salvar Alterações"):
            campos["prox_sessao"] = str(campos["prox_sessao"])
            campos["data_nascimento"] = str(campos["data_nascimento"])
            campos["inicio_tratamento"] = str(campos["inicio_tratamento"])
            campos["fim_tratamento"] = str(campos["fim_tratamento"])
            # print(paciente['id'])
            response = requests.put(
                f"http://127.0.0.1:8000/home/{paciente['id']}", json=campos
            )
            
            if response.status_code == 200:
                st.success("Paciente atualizado com sucesso.")
                st.session_state["modo_edicao"] = False  # Sair do modo de edição
            else:
                st.error("Erro ao atualizar paciente.")
                st.session_state["modo_edicao"] = False
    else:
        # Campos como texto estático
        st.write(f"**Nome:** {paciente.get('nome', '')}")
        st.write(f"**Telefone:** {paciente.get('telefone', '')}")
        st.write(f"**Endereço:** {paciente.get('endereco', '')}")
        st.write(f"**E-mail:** {paciente.get('email', '')}")
        st.write(f"**Estado Civil:** {paciente.get('estado_civil', '')}")
        st.write(f"**Data de Nascimento:** {paciente.get('data_nascimento', '')}")
        st.write(f"**Condição:** {paciente.get('condicao', '')}")
        st.write(f"**Início do Tratamento:** {paciente.get('inicio_tratamento', '')}")
        st.write(f"**Fim do Tratamento:** {paciente.get('fim_tratamento', '')}")
        st.write(f"**Próxima Sessão:** {paciente.get('prox_sessao', '')}")
        st.write(f"**Horário da Próxima Sessão:** {paciente.get('hora_prox_sessao', '')}")

        if st.button("Editar"):
            st.session_state["modo_edicao"] = True  # Ativar modo de edição

def adicionar_novo_paciente():
    st.subheader("Adicionar Novo Paciente")
    with st.form(key="add_patient"):
        nome = st.text_input("Nome")
        telefone = st.text_input("Telefone")
        prox_sessao = st.date_input("Próxima Sessão")

        submitted = st.form_submit_button("Adicionar Paciente")
        if submitted:
            response = requests.post(
                "http://127.0.0.1:8000/home/adicionar_paciente",
                json={"nome": nome, "telefone": telefone, "prox_sessao": str(prox_sessao)},
            )
            if response.status_code == 200:
                st.success("Paciente adicionado com sucesso.")
            else:
                st.error("Erro ao adicionar paciente.")
