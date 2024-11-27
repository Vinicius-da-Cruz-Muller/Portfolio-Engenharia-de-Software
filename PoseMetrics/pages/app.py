import streamlit as st
import mediapipe as mp
from streamlit_navigation_bar import st_navbar
from login import exibir_login
from cadastro import exibir_cadastro
from home import exibir_home 
from indicadores import exibir_indicadores
from usuarios import exibir_usuarios
from contato import exibir_contato
from sobre import exibir_portfolio
from sessao import pagina_sessao
from relatorios import exibir_relatorio



st.set_page_config(
    page_title="Pose Metrics",
    page_icon="posemetrics_logo.png",
    layout="wide", 
    initial_sidebar_state="expanded",
)

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "home"  

if st.session_state.pagina_atual == "login":
    exibir_login()
if st.session_state.pagina_atual == "cadastro":
    exibir_cadastro()
if st.session_state.pagina_atual == "home":
    exibir_home()
if st.session_state.pagina_atual == "indicadores":
    exibir_indicadores()
if st.session_state.pagina_atual == "usuarios":
    exibir_usuarios()
if st.session_state.pagina_atual == "sessao":
    pagina_sessao()
if st.session_state.pagina_atual == "relatorios":
    exibir_relatorio()
if st.session_state.pagina_atual == "contato":
    exibir_contato()
if st.session_state.pagina_atual == "sobre":
    exibir_portfolio()
