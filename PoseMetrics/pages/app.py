import streamlit as st
import mediapipe as mp
from streamlit_navigation_bar import st_navbar
from login import exibir_login
from cadastro import exibir_cadastro
from home import exibir_home 
from indicadores import exibir_indicadores
from exercicios import exibir_exercicios
from pacientes import exibir_pacientes
from contato import exibir_contato
from sobre import exibir_portfolio
from consulta import pagina_consulta
from relatorios import exibir_relatorio
from configuracoes import exibir_configuracoes



st.set_page_config(
    page_title="Pose Metrics",
    page_icon="posemetrics_logo.png",
    layout="wide", 
    initial_sidebar_state="expanded",
)

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "login"  

if st.session_state.pagina_atual == "login":
    exibir_login()
if st.session_state.pagina_atual == "cadastro":
    exibir_cadastro()
if st.session_state.pagina_atual == "home":
    exibir_home()
if st.session_state.pagina_atual == "indicadores":
    exibir_indicadores()
if st.session_state.pagina_atual == "exercicios":
    exibir_exercicios()
if st.session_state.pagina_atual == "pacientes":
    exibir_pacientes()
if st.session_state.pagina_atual == "consulta":
    pagina_consulta()
if st.session_state.pagina_atual == "relatorios":
    exibir_relatorio()
if st.session_state.pagina_atual == "configuracoes":
    exibir_configuracoes()
if st.session_state.pagina_atual == "contato":
    exibir_contato()
if st.session_state.pagina_atual == "sobre":
    exibir_portfolio()
