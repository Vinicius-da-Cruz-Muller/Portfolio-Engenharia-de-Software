import requests
import streamlit as st

def exibir_login():
    st.title("Login")

    # Formulário de login
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        # Faz a requisição à API de login
        response = requests.post("http://127.0.0.1:8000/auth/login", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                st.success(data["message"])
                # Aqui você pode navegar para outra página
                st.session_state.pagina_atual = "home"  # Mudando a página para "home" após login
                st.rerun()  # Atualiza a página para refletir a navegação
            else:
                st.error(data["message"])
        else:
            st.error("Erro ao se comunicar com o servidor.")

    # Exibe "Novo aqui?" como texto, sem permitir input
    st.markdown("Novo aqui?")

    # Botão de cadastro
    if st.button("Cadastrar"):
        st.session_state.pagina_atual = "cadastro"  # Navega para a página de cadastro
        st.rerun()  # Atualiza a página
