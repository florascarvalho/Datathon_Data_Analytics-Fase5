import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
from gensim.models import FastText

# Carregar modelo treinado
from tensorflow.keras.models import load_model
model = load_model("modelo/modelo_mlp.h5")
scaler = joblib.load("modelo/scaler.joblib")
ft_model = FastText.load("modelo/fasttext.model")

# Encoders treinados
encoder_academico = joblib.load("modelo/encoder_academico.joblib")
encoder_ingles = joblib.load("modelo/encoder_ingles.joblib")
encoder_espanhol = joblib.load("modelo/encoder_espanhol.joblib")

# Função para vetorizar texto com FastText
def document_vector(doc):
    words = [word for word in doc if word in ft_model.wv]
    return np.mean([ft_model.wv[word] for word in words], axis=0) if words else np.zeros(ft_model.vector_size)

# Função principal de previsão
def prever_candidato(candidato_dict):
    texto = " ".join([
        candidato_dict.get("experiencias", ""),
        candidato_dict.get("endereco", ""),
        candidato_dict.get("certificacoes", ""),
        candidato_dict.get("cursos", "")
    ])

    # Se texto principal estiver vazio, usar cv_pt
    if not texto.strip():
        texto = candidato_dict.get("cv_pt", "")

    tokenized = texto.split()
    texto_ft = document_vector(tokenized).reshape(1, -1)

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
