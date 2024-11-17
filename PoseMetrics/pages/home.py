import streamlit as st

def exibir_home():
    st.title("Bem-vindo à página inicial!")
    st.write("Você está logado.")

    # Exemplo de conteúdo da página home
    if st.button("Sair"):
        st.session_state.pagina_atual = "login"  # Retorna para o login
        st.rerun()  # Atualiza a página
