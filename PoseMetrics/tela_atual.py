import streamlit as st

def exibir_home():
    # Configuração inicial da página
    st.set_page_config(page_title="Pose Metrics - Home", layout="wide")

    # Dividindo o layout superior em duas colunas
    col1, col2 = st.columns([1, 6])

    # Coluna da esquerda: Nome e logo
    # with col1:
        # st.image("https://via.placeholder.com/50", width=50)  # Ícone aleatório como logo
        # st.markdown("<h1 style='font-size:20px; margin-top:0;'>Pose Metrics</h1>", unsafe_allow_html=True)

    # Coluna da direita: Nome e foto do profissional logado
    profissional_email = "exemplo@posemetrics.com"  # Exemplo de e-mail do profissional logado
    nome_profissional = "João da Silva"
    foto_profissional = "https://via.placeholder.com/50"  # Foto fictícia

    with col2:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-end;">
                <p style="font-size:18px; margin: 0; padding-right: 10px;">{nome_profissional}</p>
                <img src="{foto_profissional}" style="border-radius:50%; width:50px; height:50px;">
            </div>
            """,
            unsafe_allow_html=True,
        )


    # Barra lateral de navegação
    with st.sidebar:
    # Exibir logo e texto alinhados
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: center;">
                <img src="https://via.placeholder.com/50" style="width:50px; margin-right:10px;">
                <h2 style="margin: 0;">Pose Metrics</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")  # Linha de separação


        # Botões de navegação
        page = st.radio(
            "Selecione uma página:",
            ["Home", "Usuários", "Indicadores"],
            index=0
        )

    # Conteúdo da página "Home"
    if page == "Home":
        st.subheader("Próximos Pacientes")
        pacientes = [
            {"nome": "Paciente 1", "prox_sessao": "2024-11-20", "hora_prox_sessao": "10:00"},
            {"nome": "Paciente 2", "prox_sessao": "2024-11-20", "hora_prox_sessao": "11:00"},
            {"nome": "Paciente 3", "prox_sessao": "2024-11-21", "hora_prox_sessao": "14:00"},
        ]  # Exemplo de lista de pacientes

        if pacientes:
            for paciente in pacientes:
                st.write(
                    f"- {paciente['nome']} "
                    f"(Próxima Sessão: {paciente['prox_sessao']}, Hora: {paciente['hora_prox_sessao']})"
                )
        else:
            st.write("Não há pacientes agendados para este profissional.")

    elif page == "Usuários":
        st.subheader("Gerenciamento de Usuários")
        st.write("Adicione, edite ou remova usuários cadastrados no sistema.")

    elif page == "Indicadores":
        st.subheader("Indicadores de Desempenho")
        st.write("Visualize os indicadores e métricas relevantes para o seu trabalho.")

    # Rodapé
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;'>© 2024 Pose Metrics. Todos os direitos reservados.</p>",
        unsafe_allow_html=True,
    )

# Exemplo de execução
if __name__ == "__main__":
    exibir_home()
