import streamlit as st

abas = st.tabs(["🧩 Metodologia", "🛠️ Pipeline", "🖥️ Código Utilizado"])

with abas[0]:  # Primeira aba
    st.header("🧩 Metodologia")

    st.markdown(
        """<hr style="border: 3px solid #007BFF;">""",
        unsafe_allow_html=True
    )
  
    st.header("Modelo MLP (Multilayer Perceptron)", divider="gray")

    st.write("""
    Para o desafio, foi proposto um modelo de Deep Learning do tipo **MLP** (Multilayer Perceptron), que é uma rede neural artificial supervisionada composta por múltiplas camadas de neurônios: 
    uma camada de entrada, uma ou mais camadas ocultas e uma camada de saída. Cada neurônio de uma camada está conectado a todos os neurônios da próxima camada.
    """)

    image_url_1 = "https://raw.githubusercontent.com/florascarvalho/Datathon_Data_Analytics-Fase5/main/streamlit/imagens/Modelo%20MLP.jpg"
    st.image(image_url_1, caption="Modelo Esquemático de uma rede MLP")  

    st.write("""
    Em nosso modelo, o MLP foi criado utilizando a biblioteca Keras, na qual cada neurônio combina dados de entrada com pesos diferentes, aplica uma função ReLU para
    transmitir o sinal para os próximos neurônios. Pode ser visualizado no trecho abaixo:
    """)

    image_url_2 = "https://raw.githubusercontent.com/florascarvalho/Datathon_Data_Analytics-Fase5/main/streamlit/imagens/Script%20MLP_Keras.jpg"
    st.image(image_url_2, caption="Script MLP com Keras") 

    st.write("""
    Para o treinamento, foi utilizado 20%% dos dados da base. No processo é utilizada a técnica de retropropagação, ajustando assim os pesos com base no erro da previsão.       
    """)

    st.header("Vantagens e desvantagens", divider="gray")
    st.write("""
    Dentre as vantagens desse modelo, se destaca a ampla utilização para aprender padrões complexos, além de ser aplicável para casos não lineares.
    Porém, dependendo da base, pode exigir muito processamento e se tornar lento, além de ter o risco de aprender ruídos e exceções da base de dados.
    """)

with abas[1]:  # Segunda aba
    st.header("🛠️ Pipeline")

    st.markdown(
        """<hr style="border: 3px solid #007BFF;">""",
        unsafe_allow_html=True
    )

    st.header("Pipeline do Projeto", divider="gray")
    st.write("""
    Para desenvolver o modelo proposto de forma mais organizada e clara, foi montado um pipeline. Abaixo, segue o racional utilizado:
    """)

    st.markdown(""" 
    🛠️ Pipeline de Processamento e Treinamento  
    1. Instalação das bibliotecas necessárias para o processamento dos dados;  
    2. Leitura das bases de dados e unificação das mesmas, para maior eficiência no processamento;  
    3. Pré-processamento textual, no qual os campos “experiencias”, “endereco”, “certificacoes”, “cursos” são concatenados. Em caso do retorno for vazio, é utilizado o conteúdo da coluna "cv_pt" como fallback;  
    4. Label Encoding dos campos de idiomas e níveis de escolaridade, onde cada resposta terá um valor numérico atribuído à ela, possibilitando a utilização no modelo de MLP;  
    5. Tokenizar o texto concatenado, dividindo-os em palavras para auxiliar na vetorização dos mesmos com FastText;  
    6. Concatenação das variáveis, para compor uma única variável "X";  
    7. Divisão de treino e teste;  
    8. Treinamento da rede neural MLP;  
    9. Avaliação do modelo, incluindo a previsão de acurácia e perda;  
    10. Criação da função "prever candidato", recebendo os dados e calculando se um candidato deve ser chamado ou não para a entrevista, com os possíveis retornos de respostas:  
        - ❌ Reprovado  
        - 🟡 Chamar para entrevista — aderência mínima  
        - ✅ Chamar para entrevista — alta aderência  
    """)

with abas[2]:  # Terceira aba
    st.header("🖥️ Código Utilizado")

    st.markdown(
        """<hr style="border: 3px solid #007BFF;">""",
        unsafe_allow_html=True
    )

    st.header("Notebook Utilizado em PDF", divider="gray")

    pdf_path = "streamlit/PDF - Ferramenta Recrutamento_Datathon.pdf"

    try:
        with open(pdf_path, "rb") as file:
            pdf_bytes = file.read()
            st.download_button("📥 Baixar o PDF", pdf_bytes, "notebook.pdf", "application/pdf")

        # ⚠️ Observação: iframe com caminho local pode não funcionar na web — recomendável usar embed externo
        st.components.v1.iframe(f"file:///{pdf_path}", width=700, height=500)

    except FileNotFoundError:
        st.error("Arquivo PDF não encontrado. Verifique o caminho e o nome do arquivo.")

# Rodapé no sidebar
st.sidebar.success("🎓 Aluna: Flora Serafim de Carvalho | RM: RM354000")

