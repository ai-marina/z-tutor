
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# ---------------------------
# Load ESG ETF Data
# ---------------------------
etf_df = pd.read_csv("data_4908_20250720.csv", encoding="cp949")
etf_df["esg_text"] = etf_df["종목명"] + "는 " + etf_df["기초지수_지수명"] + " 지수를 추종합니다."
etf_docs = etf_df["esg_text"].tolist()

# ---------------------------
# Load ESG News Data
# ---------------------------
news_df = pd.read_csv("news_sample.csv", encoding="utf-8")
news_docs = news_df["content"].tolist()

# ---------------------------
# Embedding Models
# ---------------------------
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
etf_embeddings = embed_model.encode(etf_docs)
news_embeddings = embed_model.encode(news_docs)

# ---------------------------
# Unified Retrieval
# ---------------------------
def retrieve_top_k(query, top_k=5):
    query_vec = embed_model.encode([query])

    etf_scores = cosine_similarity(query_vec, etf_embeddings)[0]
    news_scores = cosine_similarity(query_vec, news_embeddings)[0]

    etf_ranked = sorted(zip(etf_scores, etf_docs), reverse=True)[:top_k]
    news_ranked = sorted(zip(news_scores, news_docs), reverse=True)[:top_k]

    combined_docs = [doc for _, doc in (etf_ranked + news_ranked)]
    return combined_docs

# ---------------------------
# Generate System Message
# ---------------------------
def generate_system_message(user_profile):
    return (
        f"당신은 금융 초보자를 위한 맞춤형 상담가입니다. "
        f"사용자는 '{user_profile.get('risk_type')}' 성향이며, "
        f"목표는 '{user_profile.get('goal')}', "
        f"예산은 '{user_profile.get('budget')}', "
        f"관심 분야는 '{user_profile.get('interest')}'입니다. "
        f"쉬운 용어와 친절한 말투로 대답해 주세요."
    )

# ---------------------------
# HyperCLOVA X API Call
# ---------------------------
def call_hyperclova_x(user_query, context_docs, system_message):
    url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
    headers = {
        "Authorization": "Bearer nv-50bf48a41b1848c09b1c77f84d75cd5bsZTj",
        "Content-Type": "application/json"
    }
    prompt = "[질문]\n" + user_query + "\n\n[참고 문서]\n" + "\n".join(context_docs)

    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "topP": 0.8,
        "maxTokens": 1024,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["result"]["message"]["content"]

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    user_profile = {
        "risk_type": "안정형",
        "goal": "노후 준비",
        "budget": "1,000만 원",
        "interest": "배당주, ESG ETF"
    }
    system_msg = generate_system_message(user_profile)
    question = "지금 투자하기 좋은 ETF가 뭐야?"
    docs = retrieve_top_k(question)
    result = call_hyperclova_x(question, docs, system_msg)
    print(result)
