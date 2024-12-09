import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser


def exibir_relatorio():
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
        st.session_state.pagina_atual = "consulta"  
        st.rerun()
    if selected == "Relatórios":
        pass
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
        st.title("Relatórios")
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
            # st.header(f"Bem-vindo, {nome_profissional}!")
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
                
                paciente_nome = st.selectbox(f"{nome_profissional}, selecione um paciente para visualizar o relatório", df_pacientes['nome'])

                
                paciente_selecionado = df_pacientes[df_pacientes['nome'] == paciente_nome].iloc[0]
                    
            else:
                st.write("Não há pacientes agendados para este profissional.")
        else:
            st.error("Erro ao carregar a lista de pacientes.")

        
        response_sessoes = requests.get(
            f"http://127.0.0.1:8000/home/pacientes/{paciente_selecionado['id']}/sessoes"
        )

        if response_sessoes.status_code == 200:
            sessoes = response_sessoes.json()

            if isinstance(sessoes, list) and sessoes:  # Verifica se é uma lista e não está vazia
                df_sessoes = pd.DataFrame(sessoes)
                # st.dataframe(df_sessoes)

                # Obter séries
                ids_sessoes = df_sessoes['id'].tolist()
                ids_str = ','.join(map(str, ids_sessoes))
                # st.write(ids_str)
                response_series = requests.get(f"http://127.0.0.1:8000/home/series/filtrar/{ids_str}")

                if response_series.status_code == 200:
                    series = response_series.json()
                    if isinstance(series, list) and series:
                        df_series = pd.DataFrame(series)

                        # Obter os exercícios
                        exercicio_ids = df_series['exercicio_id'].unique()  # Obter todos os IDs de exercícios únicos
                        exercicio_ids_str = ','.join(map(str, exercicio_ids))
                        # st.write(exercicio_ids_str)
                        response_exercicios = requests.get(
                            f"http://127.0.0.1:8000/home/exercicios/filtrar/{exercicio_ids_str}"
                        )

                        if response_exercicios.status_code == 200:
                            exercicios = response_exercicios.json()
                            if isinstance(exercicios, list) and exercicios:
                                df_exercicios = pd.DataFrame(exercicios)

                                # Associar os dados dos exercícios às séries
                                with st.expander("Dataset do paciente", expanded = False):
                                    df_series = df_series.merge(df_exercicios, left_on='exercicio_id', right_on='id', suffixes=('_serie', '_exercicio'))
                                    st.dataframe(df_series)
                                
                                # Criar dataset consolidado
                                dataset = pd.merge(
                                    df_series,
                                    df_sessoes,
                                    left_on="sessao_id",
                                    right_on="id",
                                    suffixes=('_serie', '_sessao')
                                )
                                

                                st.write("Duração das sessões")
                                df_sessoes['data_sessao'] = pd.to_datetime(df_sessoes['data_sessao'])
                                df_sessoes_grouped = df_sessoes.groupby('data_sessao')['tempo_total'].sum().reset_index()
                                st.line_chart(df_sessoes_grouped.set_index('data_sessao')['tempo_total'])


                                st.write("Acompanhamento por sessão")

                                col3, col4 = st.columns([0.6, 0.4])
                                with col3:
                                    sessoes = dataset['data_sessao'].unique()
                                    sessao_selecionada = st.selectbox('Escolha a Sessão:', sessoes)

                                with col4:
                                    series_sessao = dataset[dataset['data_sessao'] == sessao_selecionada]['numero_serie'].unique()
                                    serie_selecionada = st.selectbox('Escolha a Série:', series_sessao)

                                df_series_selecionada = dataset[(dataset['data_sessao'] == sessao_selecionada) & 
                                                                (dataset['numero_serie'] == serie_selecionada)]

                                df_series_selecionada = df_series_selecionada.sort_values(by='tempo')

                                df_series_selecionada['ponto_numeric'] = df_series_selecionada['ponto'].apply(lambda x: 1 if x == 'Cima' else 0)

                                st.line_chart(df_series_selecionada.set_index('tempo')['ponto_numeric'], use_container_width=True)

                            
                            else:
                                st.warning("Nenhum exercício encontrado para as séries do paciente.")
                        else:
                            st.error(f"Erro ao carregar os exercícios. Status code: {response_exercicios.status_code}")
                    else:
                        st.warning("Nenhuma série encontrada para as sessões do paciente.")
                else:
                    st.error(f"Erro ao carregar as séries das sessões. Status code: {response_series.status_code}")
            else:
                st.warning("Nenhuma sessão encontrada para este paciente.")
        else:
            st.error("Erro ao carregar as sessões do paciente.")

        
  
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
