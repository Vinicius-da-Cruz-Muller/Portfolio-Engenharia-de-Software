import streamlit as st
import requests

# Função para adicionar um novo paciente
def adicionar_novo_paciente():
    st.title("Adicionar Novo Paciente")  # Título da página
    
    with st.form("my_form"):  # Formulário para inserção dos dados
        nome = st.text_input("Nome")
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail")
        estado_civil = st.text_input("Estado Civil")
        data_nascimento = st.date_input("Data de Nascimento")
        endereco = st.text_input("Endereço")
        condicao = st.text_input("Condição do Paciente")
        inicio_tratamento = st.date_input("Início do Tratamento")
        fim_tratamento = st.date_input("Fim do Tratamento")
        prox_sessao = st.date_input("Próxima Sessão")
        hora_prox_sessao = st.text_input("Horário da Próxima Sessão (HH:MM)")
        
        # Profissional responsável (para testar, usaremos um valor fixo)
        profissional_email = "vinivini@gmail.com"
        
        # Botão para enviar o formulário
        submitted = st.form_submit_button("Adicionar Paciente")
        
        if submitted:
            if not nome or not telefone or not email:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Preparar os dados para enviar
                paciente_data = {
                    "nome": nome,
                    "telefone": telefone,
                    "email": email,
                    "estado_civil": estado_civil,
                    "data_nascimento": str(data_nascimento),
                    "endereco": endereco,
                    "condicao": condicao,
                    "inicio_tratamento": str(inicio_tratamento),
                    "fim_tratamento": str(fim_tratamento),
                    "prox_sessao": str(prox_sessao),
                    "hora_prox_sessao": hora_prox_sessao,
                    "atendente": profissional_email
                }
                
                # Fazer a requisição para a API
                response = requests.post(
                    f"http://127.0.0.1:8000/home/{profissional_email}/adicionar_paciente",
                    json=paciente_data,
                )

                if response.status_code == 200:
                    st.success("Paciente adicionado com sucesso.")
                else:
                    st.error("Erro ao adicionar paciente. Verifique os dados e tente novamente.")

# Chamar a função para adicionar paciente
if __name__ == "__main__":
    adicionar_novo_paciente()
