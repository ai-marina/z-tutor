# rag_agent.py

import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# 1. Load data
etf_df = pd.read_csv("data_4908_20250720.csv")  # 이 파일명 정확히 확인

# 2. Embed model
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 3. Precompute embeddings
esg_docs = etf_df["esg_text"].tolist()  # 이 컬럼명 정확히 확인 필요
esg_embeddings = embed_model.encode(esg_docs)

# 4. Retrieve top-k
def retrieve_top_k(query, docs, embeddings, top_k=3):
    query_vec = embed_model.encode([query])
    scores = cosine_similarity(query_vec, embeddings)[0]
    top_indices = scores.argsort()[::-1][:top_k]
    return [docs[i] for i in top_indices]

# 5. HyperCLOVA X 호출
def call_hyperclova_x(user_query, context_docs):
    url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # 🔁 반드시 Bearer 붙이기
        "Content-Type": "application/json"
    }
    prompt = (
        f"다음은 사용자의 질문과 참고 문서입니다.\n\n"
        f"[질문]\n{user_query}\n\n"
        f"[참고 문서]\n" + "\n".join(context_docs)
    )
    payload = {
        "messages": [
            {"role": "system", "content": "금융 전문가로 행동하세요."},
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
