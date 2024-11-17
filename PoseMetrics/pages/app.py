import streamlit as st
from login import exibir_login
from cadastro import exibir_cadastro
from home import exibir_home  # Página de exemplo para quando o login é bem-sucedido

# Controle de navegação
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "login"  # Define a página inicial como login

# Lógica para alternar entre as páginas
if st.session_state.pagina_atual == "login":
    exibir_login()
elif st.session_state.pagina_atual == "cadastro":
    exibir_cadastro()
elif st.session_state.pagina_atual == "home":
    exibir_home()  # Exibe a página home após login bem-sucedido
