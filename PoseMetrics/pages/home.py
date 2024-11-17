import streamlit as st
import requests

def exibir_home():
    st.title("Tela Inicial")

    # Obtem o e-mail do profissional logado
    profissional_email = st.session_state.get("email_profissional", None)

    if not profissional_email:
        st.error("Você precisa estar logado como profissional.")
        return

    response_profissional = requests.get(
        f"http://127.0.0.1:8000/home/{profissional_email}"
    )

    if response_profissional.status_code == 200:
        profissional = response_profissional.json()
        nome_profissional = profissional["nome_completo"]
        # foto_profissional = profissional["foto"]

        # st.image(foto_profissional, width=100)
        st.subheader(f"Bem-vindo, {nome_profissional}!")
    else:
        st.error("Erro ao carregar as informações do profissional.")
        return

    response_pacientes = requests.get(
        f"http://127.0.0.1:8000/home/{profissional_email}/proximos_pacientes"
    )

    if response_pacientes.status_code == 200:
        pacientes = response_pacientes.json()
        if pacientes:
            st.subheader("Próximos Pacientes:")
            for paciente in pacientes:
                st.write(
                    f"- {paciente['nome']} "
                    f"(Próxima Sessão: {paciente['prox_sessao']}, Hora: {paciente['hora_prox_sessao']})"
                )
        else:
            st.write("Não há pacientes agendados para este profissional.")
    else:
        st.error("Erro ao carregar a lista de pacientes.")
