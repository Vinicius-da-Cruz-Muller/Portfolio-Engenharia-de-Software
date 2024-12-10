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
Este projeto é parte do Trabalho de Conclusão de Curso de Engenharia de Software, apresentado à Católica de Santa Catarina, com entrega prevista para o final do segundo semestre de 2024 (10 de dezembro).

## Objetivo
O objetivo do projeto é desenvolver e validar uma ferramenta baseada em visão computacional para a análise da execução de exercícios fisioterápicos. A ferramenta visa auxiliar fisioterapeutas no acompanhamento da evolução dos pacientes, fornecendo dados quantitativos e qualitativos que melhorem a personalização e a precisão do tratamento, ao mesmo tempo em que garante uma boa performance para atender às necessidades de tempo real e precisão na análise dos movimentos dos pacientes.

## Motivação do Projeto
A falta de ferramentas acessíveis e objetivas para medir o desempenho dos pacientes em sessões de fisioterapia pode levar a avaliações subjetivas e inconsistentes. Com a crescente demanda por soluções tecnológicas em saúde, o projeto busca preencher essa lacuna, oferecendo um sistema automatizado e confiável que agrega valor para profissionais e pacientes.

## Funcionalidades
- **Captura e análise de vídeo**: Utiliza câmeras para capturar e processar os movimentos do paciente em tempo real.
- **Detecção de landmarks (pontos de referência)**: Emprega técnicas de visão computacional para rastrear articulações e movimentos utilizando o MediaPipe.
- **Análise de padrões de movimento**: Identifica desvios ou limitações em comparação a padrões ideais.
- **Geração de relatórios personalizados**: Produz relatórios detalhados com métricas como amplitude de movimento, tempo de execução e outras variáveis relevantes.
- **Gestão de usuários**: Oferece login, gerenciamento de pacientes e histórico de sessões para acompanhamento contínuo.
- **Mapas e informações correlatas**: Exibe localização dos pacientes ativos e informações climáticas.

## Benefícios
- **Aumento da precisão**: Fornecer dados objetivos e quantificáveis sobre o desempenho do paciente, reduzindo a subjetividade da avaliação manual.
- **Personalização do tratamento**: Permitir a criação de planos de tratamento mais personalizados e eficazes.

## Limitações
- **Tipo de análise**: Inicialmente, a ferramenta estará focada em um número específico de ângulos, podendo ser expandida no futuro.
- **Condições ambientais**: A precisão da análise pode ser afetada por condições de iluminação, qualidade da captura e processamento do dispositivo.
- **Variações individuais**: A ferramenta levará em consideração as características individuais de cada paciente, mas pode não ser capaz de detectar todas as nuances do movimento humano.

## Público-alvo
- Fisioterapeutas de diversas especialidades.
- Clínicas e hospitais.
- Centros de reabilitação.
- Atletas e treinadores.

## Requisitos Funcionais
- **RF1**: Permitir que o paciente realize exercícios de fisioterapia monitorados por visão computacional, com auxílio profissional.
- **RF2**: Fornecer feedback ao usuário sobre a qualidade da execução dos exercícios.
- **RF3**: Permitir que o fisioterapeuta monitore o progresso do usuário, fornecendo relatórios detalhados sobre a evolução do paciente.
- **RF4**: Ser acessível a pessoas com diferentes níveis de conhecimento técnico.
- **RF5**: Fornecer sugestões de exercícios para a prescrição pelo profissional da saúde.

## Requisitos Não Funcionais
- **NF1**: A ferramenta deve ser segura e confiável, protegendo os dados dos pacientes.
- **NF2**: A ferramenta deve ser eficiente e ter um bom desempenho.
- **NF3**: A ferramenta deve ser fácil de usar e intuitiva.
- **NF4**: A ferramenta deve ser escalável e modular, permitindo a adição de novas funcionalidades no futuro.
- **NF5**: A ferramenta deve ser compatível com diferentes dispositivos e plataformas.
- **NF6**: A ferramenta deve ser acessível a pessoas com deficiências (motoras).

## Tecnologias Utilizadas
- **MediaPipe**: Framework de visão computacional para detecção e rastreamento de landmarks no corpo humano.
- **OpenCV**: Biblioteca de processamento de imagens e vídeos.
- **Streamlit**: Framework de desenvolvimento de interfaces web interativas.
- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **PostgreSQL e Psycopg2**: Banco de dados relacional para armazenar informações de usuários e sessões.
- **Pandas e NumPy**: Bibliotecas para manipulação e análise de dados.
- **Geopy e Folium**: Ferramentas para geocodificação e visualização de mapas interativos.

## Requisitos do Projeto
- **Python 3.10+**.
- Instalação das dependências listadas no arquivo `requirements.txt`.
- Banco de dados PostgreSQL configurado com as tabelas necessárias (descritas na documentação do projeto).
- Ferramenta Git para controle de versão.
- Ambiente de desenvolvimento local ou servidor para hospedagem das aplicações.

## Arquitetura do Projeto
- **Backend**: Desenvolvido com FastAPI, gerencia as rotas de API e o acesso ao banco de dados PostgreSQL.
- **Frontend**: Interface de usuário construída em Streamlit, permite interatividade e visualização de dados.
- **Camada de Visão Computacional**: Implementada com MediaPipe e OpenCV para análise dos vídeos e extração de landmarks.
- **Banco de Dados**: PostgreSQL para armazenar informações de usuários, sessões e métricas.

## Metodologia de Organização
- **Kanban**: Utilizado para organização das tarefas no projeto, através da ferramenta Trello, monitorado com etiquetas como Fazer, Fazendo e Feito, e etapas como Backlog, Desenvolvimento e Validação.
- **FDD (Feature-Driven Development)**: Aplicado para focar em funcionalidades específicas durante cada ciclo de desenvolvimento, de forma a agregar valor a cada nova entrega.
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


