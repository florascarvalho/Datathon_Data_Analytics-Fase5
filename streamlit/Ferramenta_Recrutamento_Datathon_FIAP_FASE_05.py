import numpy as np
import joblib
from gensim.models import FastText

# Carregar recursos
model = joblib.load("OneDrive/Documentos/GitHub/Postech_Data-Analytics_Datathon_Fase5/streamlit/modelo/modelo_treinado.joblib")
scaler = joblib.load("OneDrive/Documentos/GitHub/Postech_Data-Analytics_Datathon_Fase5/streamlit/modelo/scaler.joblib")
ft_model = FastText.load("OneDrive/Documentos/GitHub/Postech_Data-Analytics_Datathon_Fase5/streamlit/modelo/fasttext.model")

encoder_academico = joblib.load("OneDrive/Documentos/GitHub/Postech_Data-Analytics_Datathon_Fase5/streamlit/modelo/encoder_academico.joblib")
encoder_ingles = joblib.load("OneDrive/Documentos/GitHub/Postech_Data-Analytics_Datathon_Fase5/streamlit/modelo/encoder_ingles.joblib")
encoder_espanhol = joblib.load("OneDrive/Documentos/GitHub/Postech_Data-Analytics_Datathon_Fase5/streamlit/modelo/encoder_espanhol.joblib")

def document_vector(doc):
    words = [word for word in doc if word in ft_model.wv]
    return np.mean([ft_model.wv[word] for word in words], axis=0) if words else np.zeros(ft_model.vector_size)

def prever_candidato(candidato_dict):
    texto = " ".join([
        candidato_dict.get("experiencias", ""),
        candidato_dict.get("endereco", ""),
        candidato_dict.get("certificacoes", ""),
        candidato_dict.get("cursos", "")
    ])

    if not texto.strip():
        texto = candidato_dict.get("cv_pt", "")

    tokenized = texto.split()
    texto_ft = document_vector(tokenized).reshape(1, -1)

    nivel_academico = candidato_dict.get("nivel_academico", "")
    nivel_ingles = candidato_dict.get("nivel_ingles", "")
    nivel_espanhol = candidato_dict.get("nivel_espanhol", "")

   
    if nivel_academico not in encoder_academico.classes_:
        nivel_academico = encoder_academico.classes_[0]  # ou exiba mensagem de aviso

    if nivel_ingles not in encoder_ingles.classes_:
        nivel_ingles = encoder_ingles.classes_[0]

    if nivel_espanhol not in encoder_espanhol.classes_:
        nivel_espanhol = encoder_espanhol.classes_[0]

    try:
        nivel_academico = encoder_academico.transform([candidato_dict.get("nivel_academico", "")])[0]
        nivel_ingles = encoder_ingles.transform([candidato_dict.get("nivel_ingles", "")])[0]
        nivel_espanhol = encoder_espanhol.transform([candidato_dict.get("nivel_espanhol", "")])[0]
        
    except Exception as e:
        return f"Erro ao codificar os atributos estruturados: {e}"

    atributos = scaler.transform([[nivel_academico, nivel_ingles, nivel_espanhol]])
    X_novo = np.hstack([texto_ft, atributos])

    prob = model.predict(X_novo)[0][0]

    if prob < 0.15:
        return "❌ Reprovado — Candidato não possui aderência."
    elif prob < 0.6:
        return "🟡 Chamar para entrevista — Aderência mínima e chances moderadas."
    else:
        return "✅ Chamar para entrevista — Alta aderência e boas chances."
