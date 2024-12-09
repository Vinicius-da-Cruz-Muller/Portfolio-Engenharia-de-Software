import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap

geolocator = Nominatim(user_agent="posemetrics_app_v1")


def exibir_indicadores():
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
        pass
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
        st.title("Indicadores")
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
        
        valid_coords = []
        if response_pacientes.status_code == 200:
            pacientes = response_pacientes.json()
            if pacientes:
                df_pacientes = pd.DataFrame(pacientes)
                pacientes_ativos = df_pacientes[df_pacientes['status'] == True]
                # Colunas que você deseja exibir
                colunas_exibir = ['nome', 'endereco', 'telefone', 'condicao']  # Substitua pelos nomes das colunas desejadas

                # Verificando se as colunas existem no DataFrame para evitar erros
                colunas_existentes = [col for col in colunas_exibir if col in df_pacientes.columns]
                df_exibir = pacientes_ativos[colunas_exibir]

                # Exibindo apenas as colunas selecionadas
                with st.expander("Seus pacientes", expanded = False):
                    st.dataframe(df_exibir)

                for index, row in df_pacientes.iterrows():
                    endereco = row['endereco']
                    latitude, longitude = geocode_address(endereco)
                    if latitude and longitude:  # Endereço válido
                        valid_coords.append([latitude, longitude])
                    else:
                        st.warning(f"Endereço inválido ou não encontrado: {endereco}")


                # Contando pacientes ativos
                pacientes_ativos = df_pacientes[df_pacientes['status'] == True].shape[0]

                # Obtendo condições únicas
                condicoes_tratadas = df_pacientes['condicao'].unique()

                # Exibindo os resultados
                col_total, col_condicao = st.columns([0.2, 0.8])
                with col_total:
                    st.write(f"Total de pacientes ativos: {pacientes_ativos}")
                with col_condicao:
                    with st.expander("Condições que você acompanha", expanded=False):
                        st.write("Condições tratadas:")
                        for condicao in condicoes_tratadas:
                            st.write(f"- {condicao}")

                if valid_coords:
                    # Criação do mapa centrado na média das coordenadas validadas
                    mean_lat = sum(coord[0] for coord in valid_coords) / len(valid_coords)
                    mean_lon = sum(coord[1] for coord in valid_coords) / len(valid_coords)
                    mapa = folium.Map(location=[mean_lat, mean_lon], zoom_start=12)

                    # Adicionando marcadores para cada coordenada válida
                    for coord in valid_coords:
                        folium.Marker(location=coord, icon=folium.Icon(color='blue')).add_to(mapa)

                    # Exibindo o mapa no Streamlit
                    st.subheader("Mapa de Pacientes")
                    st.components.v1.html(mapa._repr_html_(), height=600)
                else:
                    st.warning("Não foi possível encontrar nenhum endereço válido para os pacientes.")

                
                # Exibindo mapa de calor
                if valid_coords:
                    mapa = folium.Map(location=[df_pacientes['latitude'].mean(), df_pacientes['longitude'].mean()], zoom_start=12)
                    HeatMap(valid_coords).add_to(mapa)
                    st.write("Mapa de Densidade de Pacientes")
                    st.components.v1.html(mapa._repr_html_(), height=600)
                else:
                    st.warning("Não foi possível encontrar nenhum endereço válido para os pacientes.")

                    
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


def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None