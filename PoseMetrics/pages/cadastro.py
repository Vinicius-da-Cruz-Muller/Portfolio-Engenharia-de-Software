import streamlit as st

def exibir_cadastro():
    st.title("Cadastro")
    st.text_input("Nome")
    st.text_input("E-mail")
    st.text_input("Senha", type="password")
    
    if st.button("Cadastrar"):
        st.success("Usuário cadastrado com sucesso!")
        st.session_state.pagina_atual = "login"
        st.experimental_rerun()
