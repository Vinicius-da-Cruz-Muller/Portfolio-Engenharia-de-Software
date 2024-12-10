import streamlit as st
import requests
from streamlit_option_menu import option_menu


def exibir_contato():

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
        st.session_state.pagina_atual = "relatorios"  
        st.rerun()
    if selected == "Configurações":
        st.session_state.pagina_atual = "configuracoes"  
        st.rerun()
    if selected == "Contato":
        pass
    if selected == "Sobre":
        st.session_state.pagina_atual = "sobre"
        st.rerun()

    st.title("Entre em Contato!")

    st.markdown(
        """
        <style>
        .contact-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 20px;
            margin: 10px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            color: #00ff00;
        }
        .instagram { background-color: #E1306C60; color: white; }
        .linkedin { background-color: #0077B560; color: white; }
        .github { background-color: #33333360; color: white; }
        .contact-button:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <a href="https://www.instagram.com/viniciuscmuller/" target="_blank" class="contact-button instagram">
                Instagram
            </a>
            <p>Me acompanhe no Instagram!</p>
            <p>Quer saber mais sobre mim e acompanhar minhas atualizações? Busque terapia!</p>
            """,
            unsafe_allow_html=True,
        )


    with col2:
        st.markdown(
            """
            <a href="https://www.linkedin.com/in/vin%C3%ADcius-da-cruz-muller-738784170/" target="_blank" class="contact-button linkedin">
                LinkedIn
            </a>
            <p>Conecte-se comigo no LinkedIn!</P>
            <p>Quer saber mais sobre minha trajetória profissional e projetos? Vamos nos conectar no LinkedIn!</p>
            """,
            unsafe_allow_html=True,
        )


    with col3:
        st.markdown(
            """
            <a href="https://github.com/Vinicius-da-Cruz-Muller" target="_blank" class="contact-button github">
                GitHub
            </a>
            <p>Confira meus projetos no GitHub!</p>
            <p>Explore meus repositórios e veja o que tenho desenvolvido!</p>
            """,
            unsafe_allow_html=True,
        )

