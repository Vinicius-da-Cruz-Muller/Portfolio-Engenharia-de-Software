import streamlit as st
from streamlit_option_menu import option_menu

def exibir_portfolio():

    with st.sidebar:
        st.logo("posemetrics_logo.png", size="large", link=None, icon_image=None)
        selected = option_menu(
            menu_title = None,
            options = ["Home", "Indicadores", "Exercícios", "Pacientes", "Consulta", "Relatórios", "Configurações", "Contato", "Sobre"],
            icons=['house', 'graph-up-arrow', 'heart-pulse', 'people', 'calendar2-heart', 'bar-chart', 'gear', 'github', 'question-circle'], 
            # menu_icon="menu-button-wide-fill", 
            # default_index=0
            styles={
            "container": {"background-color": "#4E937A60"},  
            "icon": {"color": "#A22C29", "font-size": "20px"},  
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "10px",
                "--hover-color": "#A22C2960",
            },
            "nav-link-selected": {"background-color": "#4E937A90", "color": "white"},
        },
        )

    if selected == "Home":
        st.session_state.pagina_atual = "home"
        st.rerun()
    if selected == "Indicadores":
        st.session_state.pagina_atual = "indicadores"  
        st.rerun()
    if selected == "Exercícios":
        st.session_state.pagina_atual = "exercicios"  
        st.rerun()
    if selected == "Pacientes":
        st.session_state.pagina_atual = "pacientes"  
        st.rerun()
    if selected == "Consulta":
        st.session_state.pagina_atual = "consulta"  
        st.rerun()
    if selected == "Relatórios":
        st.session_state.pagina_atual = "relatorios"  
        st.rerun()
    if selected == "Configurações":
        st.session_state.pagina_atual = "configuracoes"  
        st.rerun()
    if selected == "Contato":
        st.session_state.pagina_atual = "contato"
        st.rerun()
    if selected == "Sobre":
        pass


    st.title("Portfólio Engenharia de Software")
    st.markdown(
    """
    Trabalho de Conclusão de Curso de Engenharia de Software, da Católica de Santa Catarina, a ser entregue no final do segundo semestre de 2024.
    """
    )

    st.markdown(
    """
    ## Objetivo:
    Desenvolver e validar uma ferramenta que utilize técnicas de visão computacional para analisar a execução de exercícios fisioterápicos. A ferramenta tem como objetivo principal auxiliar fisioterapeutas no acompanhamento e avaliação da evolução dos pacientes, fornecendo dados quantitativos e qualitativos sobre o desempenho do paciente em cada sessão.
    """
    )

    st.markdown(
    """
    ## Funcionalidades:
    - **Captura e análise de vídeo**: Capturar vídeos da execução dos exercícios, utilizando câmeras convencionais ou dispositivos móveis.
    - **Detecção e rastreamento de pontos-chave**: Identificar e rastrear pontos-chave do corpo humano nos vídeos, como articulações e membros, para analisar a amplitude de movimento, alinhamento postural e outras métricas relevantes.
    - **Reconhecimento de padrões de movimento**: Comparar os movimentos realizados pelo paciente com padrões de referência, identificando desvios e ineficiências.
    - **Geração de relatórios**: Gerar relatórios detalhados sobre o desempenho do paciente, incluindo métricas quantitativas (ângulos, distâncias, tempo) e qualitativas (descrição de movimentos, identificação de erros).
    - **Interface intuitiva**: Desenvolver uma interface amigável para fisioterapeutas, permitindo a fácil configuração e utilização da ferramenta.
    """
    )

    st.markdown(
    """
    ## Limitações:
    - **Tipos de exercícios**: Inicialmente, a ferramenta estará focada em um conjunto específico de exercícios, podendo ser expandida para outros tipos no futuro.
    - **Condições ambientais**: A precisão da análise pode ser afetada por condições de iluminação, vestimentas do paciente e outros fatores ambientais.
    - **Variações individuais**: A ferramenta levará em consideração as características individuais de cada paciente, mas pode não ser capaz de detectar todas as nuances do movimento humano.
    """
    )

    st.markdown(
    """
    ## Público-alvo:
    - Fisioterapeutas de diversas especialidades.
    - Clínicas e hospitais.
    - Centros de reabilitação.
    - Atletas e treinadores.
    """
    )

    st.markdown(
    """
    ## Benefícios:
    - **Aumento da precisão**: Fornecer dados objetivos e quantificáveis sobre o desempenho do paciente, reduzindo a subjetividade da avaliação manual.
    - **Melhora da eficiência**: Automatizar tarefas repetitivas, liberando o fisioterapeuta para focar em atividades de maior valor agregado.
    - **Personalização do tratamento**: Permitir a criação de planos de tratamento mais personalizados e eficazes.
    """
    )

    st.markdown(
    """
    ### Responder ao longo do desenvolvimento:
    - **Metodologia de validação**: Como validar a precisão e a confiabilidade da ferramenta?
    - **Dados**: Quais tipos de dados serão coletados e como eles serão armazenados e protegidos?
    - **Integração com outros sistemas**: Como a ferramenta se integrará com outros sistemas utilizados na clínica, como prontuários eletrônicos?
    - **Escalabilidade**: Como a ferramenta pode ser expandida para atender a um número maior de usuários e tipos de exercícios?
    """
    )

import streamlit as st

st.title("Portfólio Engenharia de Software")
st.markdown(
    """
    Este projeto é parte do Trabalho de Conclusão de Curso de Engenharia de Software, apresentado à Católica de Santa Catarina, com entrega prevista para o final do segundo semestre de 2024.
    """
)

st.markdown(
    """
    ## Objetivo:
    O objetivo do projeto é desenvolver e validar uma ferramenta baseada em visão computacional para a análise da execução de exercícios fisioterápicos. A ferramenta visa auxiliar fisioterapeutas no acompanhamento da evolução dos pacientes, fornecendo dados quantitativos e qualitativos que melhorem a personalização e a precisão do tratamento.
    """
)

st.markdown(
    """
    ## Motivação do Projeto:
    A falta de ferramentas acessíveis e objetivas para medir o desempenho dos pacientes em sessões de fisioterapia pode levar a avaliações subjetivas e inconsistentes. Com a crescente demanda por soluções tecnológicas em saúde, o projeto busca preencher essa lacuna, oferecendo um sistema automatizado e confiável que agrega valor para profissionais e pacientes.
    """
)

st.markdown(
    """
    ## Funcionalidades:
    - **Captura e análise de vídeo:** Utiliza câmeras para capturar e processar os movimentos do paciente em tempo real.
    - **Detecção de landmarks:** Emprega técnicas de visão computacional para rastrear articulações e movimentos utilizando o MediaPipe.
    - **Análise de padrões de movimento:** Identifica desvios ou limitações em comparação a padrões ideais.
    - **Geração de relatórios personalizados:** Produz relatórios detalhados com métricas como amplitude de movimento, tempo de execução e outras variáveis relevantes.
    - **Gestão de usuários:** Oferece login, gerenciamento de pacientes e histórico de sessões para acompanhamento contínuo.
    - **Mapas de calor e visualizações:** Exibe localização dos pacientes ativos e indicadores de densidade usando mapas interativos.
    """
)

st.markdown(
    """
    ## Tecnologias Utilizadas:
    - **MediaPipe:** Framework de visão computacional para detecção e rastreamento de landmarks no corpo humano.
    - **OpenCV:** Biblioteca de processamento de imagens e vídeos.
    - **Streamlit:** Framework de desenvolvimento de interfaces web interativas.
    - **FastAPI:** Framework para construção de APIs rápidas e eficientes.
    - **PostgreSQL e Psycopg2:** Banco de dados relacional para armazenar informações de usuários e sessões.
    - **Pandas e NumPy:** Bibliotecas para manipulação e análise de dados.
    - **Geopy e Folium:** Ferramentas para geocodificação e visualização de mapas interativos.
    """
)

st.markdown(
    """
    ## Requisitos do Projeto:
    - Python 3.10+
    - Instalação das dependências listadas no arquivo `requirements.txt`.
    - Banco de dados PostgreSQL configurado com as tabelas necessárias (descritas na documentação do projeto).
    - Ferramenta Git para controle de versão.
    - Ambiente de desenvolvimento local ou servidor para hospedagem das aplicações.
    """
)

st.markdown(
    """
    ## Arquitetura do Projeto:
    O projeto é composto por:
    - **Backend:** Desenvolvido com FastAPI, gerencia as rotas de API e o acesso ao banco de dados PostgreSQL.
    - **Frontend:** Interface de usuário construída em Streamlit, permite interatividade e visualização de dados.
    - **Camada de Visão Computacional:** Implementada com MediaPipe e OpenCV para análise dos vídeos e extração de landmarks.
    - **Banco de Dados:** PostgreSQL para armazenar informações de usuários, sessões e métricas.
    """
)

st.markdown(
    """
    ## Metodologia de Organização:
    - **Kanban:** Utilizado para organização das tarefas no projeto, dividido em etapas como `To Do`, `In Progress` e `Done`.
    - **FDD (Feature-Driven Development):** Aplicado para focar em funcionalidades específicas durante cada ciclo de desenvolvimento.
    """
)

st.markdown(
    """
    ## Guia para Novos Desenvolvedores:
    1. **Clone o repositório:**  
       ```
       git clone https://github.com/seu-usuario/seu-repositorio.git
       ```
    2. **Configure o ambiente virtual:**  
       ```
       python -m venv venv
       source venv/bin/activate  # Linux/Mac
       venv\Scripts\activate  # Windows
       ```
    3. **Instale as dependências:**  
       ```
       pip install -r requirements.txt
       ```
    4. **Configure o banco de dados PostgreSQL:**  
       - Crie as tabelas utilizando os scripts disponíveis no repositório.
       - Atualize o arquivo `config.ini` com as credenciais do banco de dados.
    5. **Inicie o servidor FastAPI:**  
       ```
       uvicorn main:app --reload
       ```
    6. **Rode o frontend no Streamlit:**  
       ```
       streamlit run app.py
       ```
    """
)

st.markdown(
    """
    ## Questões em Aberto:
    - **Validação:** Como garantir a precisão e confiabilidade dos dados coletados?
    - **Integração:** Quais são os próximos passos para integração com prontuários eletrônicos?
    - **Escalabilidade:** Como expandir o sistema para suportar mais exercícios e usuários?
    """
)

st.markdown(
    """
    ## Contato:
    - [Instagram](https://instagram.com/seu_perfil)
    - [LinkedIn](https://linkedin.com/in/seu_perfil)
    - [GitHub](https://github.com/seu-usuario)
    """
)


