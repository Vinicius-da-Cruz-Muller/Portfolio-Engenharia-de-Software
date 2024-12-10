import streamlit as st
import requests
import pandas as pd
import io
from streamlit_option_menu import option_menu
from adicionar import adicionar_novo_paciente

import base64


def exibir_pacientes():
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

        response_pacientes = requests.get(
            f"http://127.0.0.1:8000/home/{profissional_email}/listar_pacientes"
        )

        if response_pacientes.status_code == 200:
            pacientes = response_pacientes.json()
            if pacientes:
                df_pacientes = pd.DataFrame(pacientes)
                
                paciente_nome = st.selectbox("Selecione um paciente", df_pacientes['nome'])

                
                paciente_selecionado = df_pacientes[df_pacientes['nome'] == paciente_nome].iloc[0]
                editar_paciente(paciente_selecionado)
                    
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







def editar_paciente(paciente):
    
    if "modo_edicao" not in st.session_state:
        st.session_state["modo_edicao"] = False

    if st.session_state["modo_edicao"]:
        # Campos editáveis
        campos = {
            "nome": st.text_input("Nome", paciente.get("nome", "")),
            "telefone": st.text_input("Telefone", paciente.get("telefone", "")),
            "ultima_sessao": st.date_input(
                "Última sessão", pd.to_datetime(paciente.get("ultima_sessao", pd.Timestamp.now()))
            ),
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
            campos["ultima_sessao"] = str(campos["ultima_sessao"])
            campos["data_nascimento"] = str(campos["data_nascimento"])
            campos["inicio_tratamento"] = str(campos["inicio_tratamento"])
            campos["fim_tratamento"] = str(campos["fim_tratamento"])

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
        exibir_ficha_paciente(paciente)









def exibir_ficha_paciente(paciente):
    st.subheader("Ficha do Paciente")
    if paciente.get("foto"):
        # Decodifica a string Base64 para bytes
        image_bytes = io.BytesIO(base64.b64decode(paciente["foto"]))
        st.image(
            image_bytes,
            caption=f"Foto de {paciente.get('nome', 'Paciente')}",
            width=150,  # Define a largura da imagem (ajustável conforme necessário)
            use_column_width=False
        )
    else:
        st.write("Foto não disponível.")

    # Criar layout em colunas para uma apresentação mais estruturada
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Teste:** {paciente.get('foto', '')}")
        st.markdown(f"**Nome:** {paciente.get('nome', '')}")
        st.markdown(f"**Telefone:** {paciente.get('telefone', '')}")
        st.markdown(f"**Estado Civil:** {paciente.get('estado_civil', '')}")
        st.markdown(f"**Início do Tratamento:** {paciente.get('inicio_tratamento', '')}")
        st.markdown(f"**Horário da Próxima Sessão:** {paciente.get('hora_prox_sessao', '')}")
        st.markdown(f"**Condição:** {paciente.get('condicao', '')}")
        

    with col2:
        st.markdown(f"**Data de Nascimento:** {paciente.get('data_nascimento', '')}")
        st.markdown(f"**E-mail:** {paciente.get('email', '')}")
        st.markdown(f"**Endereço:** {paciente.get('endereco', '')}")
        st.markdown(f"**Fim do Tratamento:** {paciente.get('fim_tratamento', '')}")
        st.markdown(f"**Última Sessão:** {paciente.get('ultima_sessao', '')}")
        st.markdown(f"**Próxima Sessão:** {paciente.get('prox_sessao', '')}")
        


    # Botões de ações
    st.divider()
    col_edit, col_add = st.columns([0.5, 0.5])
    with col_edit:
        if st.button("Editar paciente"):
            st.session_state["modo_edicao"] = True

    with col_add:
        if st.button("Adicionar paciente"):
            st.session_state.pagina_atual = "adicionar"  
            st.rerun()

    # with col_buttons[2]:
    #     if st.button("Iniciar sessão", key="iniciar_sessao"):
    #         st.session_state.pagina_atual = "sessao"
    #         st.session_state["paciente_id"] = paciente["id"]
    #         st.rerun()





