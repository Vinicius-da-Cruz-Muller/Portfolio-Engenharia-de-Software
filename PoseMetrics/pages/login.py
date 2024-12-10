import streamlit as st
import requests

def exibir_login():
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    with col2:
        col4, col5, col6 = st.columns([0.45, 0.1, 0.45])
        with col5:
            st.image("posemetrics_logo.png", width = 100)
        st.title("Login")

        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            response = requests.post(
                "http://127.0.0.1:8000/auth/login",
                params={"email": email, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                if data["status"] == "success":
                    st.success("Login realizado com sucesso!")
                    st.session_state["email_profissional"] = email

                    st.session_state.pagina_atual = "home"  
                    st.rerun()
                else:
                    st.error("E-mail ou senha inválidos.")
            else:
                st.error(response.json().get("detail", "Erro ao se comunicar com o servidor."))
        st.markdown("Novo aqui?")

        if st.button("Cadastrar"):
            st.session_state.pagina_atual = "cadastro"  
            st.rerun()  
