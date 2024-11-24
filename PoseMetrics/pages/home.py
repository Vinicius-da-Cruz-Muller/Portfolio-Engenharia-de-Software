import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser


def exibir_home():
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
            options = ["Home", "Indicadores", "Usuários", "Contato", "Sobre"],
            icons=['house', 'graph-up-arrow', 'people', 'github'], 
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
        pass
    if selected == "Indicadores":
        st.session_state.pagina_atual = "indicadores"  
        st.rerun()
    if selected == "Usuários":
        st.session_state.pagina_atual = "usuarios"  
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
            st.header(f"Bem-vindo, {nome_profissional}!")
        else:
            st.error("Erro ao carregar as informações do profissional.")
            return

        response_pacientes = requests.get(
            f"http://127.0.0.1:8000/home/{profissional_email}/proximos_pacientes"
        )

        if response_pacientes.status_code == 200:
            pacientes = response_pacientes.json()
            if pacientes:
                df_pacientes = pd.DataFrame(pacientes)
                st.markdown(
                    """
                    <style>
                        /* Personalizando a tabela */
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            background-color: #4E937A60;  
                        }
                        table, th, td {
                            border: 1px solid #004B87;
                        }
                        th {
                            font-weight: bold;
                            color: black;  
                            text-align: left;
                            padding: 8px;
                        }
                        td {
                            padding: 8px;
                            text-align: left;
                        }
                        tr:nth-child(even) {
                            background-color: #f2f2f2;
                        }
                        tr:hover {
                            background-color: #ddd;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                st.subheader("Seus próximos atendimentos:")
                table_html = df_pacientes.to_html(classes='streamlit-table', index=False)
                st.markdown(table_html, unsafe_allow_html=True)
                # for paciente in pacientes:
                #     st.write(
                #         f"- {paciente['nome']} "
                #         f"(Próxima Sessão: {paciente['prox_sessao']}, Hora: {paciente['hora_prox_sessao']})"
                #     )
            else:
                st.write("Não há pacientes agendados para este profissional.")
        else:
            st.error("Erro ao carregar a lista de pacientes.")

        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    with col2:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-end;">
                <p style="font-size:18px; margin: 0; padding-right: 10px;">{nome_profissional}</p>
                <img src="{foto_profissional}" style="border-radius:50%; width:50px; height:50px;">
            </div>
            """,
            unsafe_allow_html=True,
        )