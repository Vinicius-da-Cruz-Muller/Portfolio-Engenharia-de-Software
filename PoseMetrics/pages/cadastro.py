import streamlit as st
import requests

def exibir_cadastro():

    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        col4, col5, col6 = st.columns([0.45, 0.1, 0.45])
        with col5:
            st.image("posemetrics_logo.png", width = 100)
        st.title("Cadastro de Usuário")
        nome = st.text_input("Nome Completo")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        confirmar_senha = st.text_input("Confirme a Senha", type="password")

        if st.button("Cadastrar"):
            if senha != confirmar_senha:
                st.error("As senhas não coincidem!")
            else:
                response = requests.post("http://127.0.0.1:8000/auth/cadastro", json={
                    "nome": nome,
                    "email": email,
                    "senha": senha
                })

                if response.status_code == 200:
                    st.success("Cadastro realizado com sucesso!")
                    st.session_state.pagina_atual = "login"  
                    st.rerun()
                else:
                    st.error(response.json().get("detail", "Erro ao cadastrar usuário."))
