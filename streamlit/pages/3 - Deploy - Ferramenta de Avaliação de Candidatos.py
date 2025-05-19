import streamlit as st
import fitz  # PyMuPDF
import numpy as np
import pandas as pd

# Carregar recursos do modelo
from streamlit.Ferramenta import prever_candidato, encoder_academico, encoder_ingles, encoder_espanhol, scaler, model

st.set_page_config(page_title="Análise de Candidato", layout="centered")
st.title("📋 Ferramenta de Avaliação de Candidatos")

# Formulário do candidato
with st.form("formulario_candidato"):
    candidato = st.text_input("Nome do Candidato")
    experiencia = st.text_area("Experiências Profissionais")
    endereco = st.text_input("Cidade")
    estado = st.text_input("Estado")
    pais = st.text_input("País")
    certificacoes = st.text_area("Certificações")
    cursos = st.text_area("Cursos Complementares")

    nivel_academico = st.selectbox("Nível Acadêmico", ["Fundamental", "Médio", "Técnico", "Graduação", "Pós-graduação", "Mestrado", "Doutorado"])
    nivel_ingles = st.selectbox("Inglês", ["Básico", "Intermediário", "Avançado", "Fluente"])
    nivel_espanhol = st.selectbox("Espanhol", ["Básico", "Intermediário", "Avançado", "Fluente"])

    uploaded_pdf = st.file_uploader("Currículo em PDF", type=["pdf"])

    submitted = st.form_submit_button("Analisar Candidato")

if submitted:
    # Ler PDF
    cv_pt = ""
    if uploaded_pdf is not None:
        with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
            for page in doc:
                cv_pt += page.get_text()

    # Montar dicionário para o modelo
    candidato_dict = {
        "cv_pt": cv_pt,
        "experiencias": experiencia,
        "endereco": f"{endereco}, {estado}, {pais}",
        "certificacoes": certificacoes,
        "cursos": cursos,
        "nivel_academico": nivel_academico,
        "nivel_ingles": nivel_ingles,
        "nivel_espanhol": nivel_espanhol
    }

    with st.spinner("Analisando perfil..."):
        resultado = prever_candidato(candidato_dict)
        st.success(f"Resultado para {candidato}: {resultado}")
