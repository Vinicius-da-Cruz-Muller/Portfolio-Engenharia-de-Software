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


