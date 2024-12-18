import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import webbrowser
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap

geolocator = Nominatim(user_agent="posemetrics_app_v1")

def obter_clima(cidade, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

API_KEY = "2447cbd5fa4a0fe9a829980416a8dd54"

CIDADE = "Jaraguá do Sul"


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
                colunas_exibir = ['nome', 'endereco', 'telefone', 'condicao'] 
                colunas_existentes = [col for col in colunas_exibir if col in df_pacientes.columns]
                df_exibir = pacientes_ativos[colunas_exibir]

                with st.expander("Seus pacientes", expanded = False):
                    st.dataframe(df_exibir)

                for index, row in df_pacientes.iterrows():
                    endereco = row['endereco']
                    latitude, longitude = geocode_address(endereco)
                    if latitude and longitude:  # Endereço válido
                        valid_coords.append([latitude, longitude])
                    else:
                        st.warning(f"Endereço inválido ou não encontrado: {endereco}")


                pacientes_ativos = df_pacientes[df_pacientes['status'] == True].shape[0]

                condicoes_tratadas = df_pacientes['condicao'].unique()

                col_total, col_condicao = st.columns([0.2, 0.8])
                with col_total:
                    st.write(f"Total de pacientes ativos: {pacientes_ativos}")
                with col_condicao:
                    with st.expander("Condições que você acompanha", expanded=False):
                        st.write("Condições tratadas:")
                        for condicao in condicoes_tratadas:
                            st.write(f"- {condicao}")

                if valid_coords:
                    mean_lat = sum(coord[0] for coord in valid_coords) / len(valid_coords)
                    mean_lon = sum(coord[1] for coord in valid_coords) / len(valid_coords)
                    mapa = folium.Map(location=[mean_lat, mean_lon], zoom_start=12)

                    for coord in valid_coords:
                        folium.Marker(location=coord, icon=folium.Icon(color='blue')).add_to(mapa)

                    st.subheader("Mapa de Pacientes")
                    st.components.v1.html(mapa._repr_html_(), height=600)
                    st.write("Utilize o mapa para verificar sua área de atuação. Clima ruim e distância do consultório são fatores relevantes na assiduidade e pontualidade do tratamento fisioterápico.")
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


def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None