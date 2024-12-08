import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser
from datetime import datetime

def obter_clima(cidade, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Substitua pela sua chave de API
API_KEY = "2447cbd5fa4a0fe9a829980416a8dd54"

# Cidade para exibir os dados
CIDADE = "Jaraguá do Sul"


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
        pass
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
                # Conversões de data/hora
                try:
                    df_pacientes['hora_prox_sessao'] = pd.to_datetime(
                        df_pacientes['hora_prox_sessao'], format='%H:%M:%S'
                    ).dt.time
                except ValueError:
                    # Caso o formato não seja '%H:%M:%S', tenta inferir automaticamente
                    df_pacientes['hora_prox_sessao'] = pd.to_datetime(
                        df_pacientes['hora_prox_sessao'], format='mixed'
                    ).dt.time

                df_pacientes['prox_sessao'] = pd.to_datetime(df_pacientes['prox_sessao'], errors='coerce')


                # Data e hora atuais
                agora = datetime.now()
                data_hoje = agora.date()
                hora_atual = agora.time()

                # Filtro: sessões a partir de hoje e horas a partir da hora atual
                df_filtrado = df_pacientes[
                    (df_pacientes['prox_sessao'].dt.date >= data_hoje) &
                    (
                        (df_pacientes['prox_sessao'].dt.date > data_hoje) |
                        (df_pacientes['hora_prox_sessao'] >= hora_atual)
                    )
                ]

                # Ordena por data e hora da próxima sessão
                df_filtrado = df_filtrado.sort_values(by=['prox_sessao', 'hora_prox_sessao'])

                # Limita a 10 pacientes
                df_filtrado = df_filtrado.head(10)
                if not df_filtrado.empty:
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
                    table_html = df_filtrado.to_html(classes='streamlit-table', index=False)
                    st.markdown(table_html, unsafe_allow_html=True)
                # for paciente in pacientes:
                #     st.write(
                #         f"- {paciente['nome']} "
                #         f"(Próxima Sessão: {paciente['prox_sessao']}, Hora: {paciente['hora_prox_sessao']})"
                #     )
                else:
                    st.write("Não há pacientes agendados a partir de hoje.")
            else:
                st.write("Não há pacientes agendados para este profissional.")
        else:
            st.error("Erro ao carregar a lista de pacientes.")

        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
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
        clima = obter_clima(CIDADE, API_KEY)
        
        if clima:
            temperatura = clima['main']['temp']
            descricao = clima['weather'][0]['description']
            icone = clima['weather'][0]['icon']
            icone_url = f"http://openweathermap.org/img/wn/{icone}.png"

            st.markdown(
            f"""
            <div style="text-align: center; "background-color: #f0f0f0;">
                <img src="{icone_url}" width="80">
                <p><strong>Cidade:</strong> {CIDADE}</p>
                <p><strong>Temperatura:</strong> {temperatura}°C</p>
                <p><strong>Descrição:</strong> {descricao.capitalize()}</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        else:
            st.error("Não foi possível obter os dados climáticos.")


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