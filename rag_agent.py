# rag_agent.py
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# 1. Load ETF data (ensure encoding and path are correct)
etf_df = pd.read_csv("data_4908_20250720.csv", encoding="cp949")
etf_df["esg_text"] = etf_df["종목명"] + "는 " + etf_df["기초지수_지수명"] + " 지수를 추조합니다."
esg_docs = etf_df["esg_text"].tolist()

# 2. Load SentenceTransformer model
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
esg_embeddings = embed_model.encode(esg_docs)

# 3. Retrieve top K relevant documents
def retrieve_top_k(query, top_k=3):
    query_vec = embed_model.encode([query])
    scores = cosine_similarity(query_vec, esg_embeddings)[0]
    top_indices = scores.argsort()[::-1][:top_k]
    return [esg_docs[i] for i in top_indices]

# 4. Call HyperCLOVA X

def call_hyperclova_x(user_query, context_docs, system_message):
    url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
    headers = {
        "Authorization": "Bearer API Key",  # 모델 key 입력
        "Content-Type": "application/json"
    }
    prompt = (
        f"[\uc9c8\ubb38]\n{user_query}\n\n" +
        f"[\ucc38\uace0 \ubb38\uc11c]\n" + "\n".join(context_docs)
    )
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
