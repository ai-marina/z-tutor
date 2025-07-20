# rag_agent.py
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# 1. Load ESG 데이터
etf_df = pd.read_csv("data_4908_20250720.csv", encoding='cp949')  # 디렉토리 반영

# 2. Sentence-BERT 임베딩 모델 로드
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 3. ESG 문서 임베딩
esg_docs = etf_df["내용"].tolist()  # 실제 컬럼명 확인 후 수정 (예: "esg_text" → "내용")
esg_embeddings = embed_model.encode(esg_docs, convert_to_tensor=False)  # numpy array

# 4. RAG: 유사 문서 top-k 검색
def retrieve_top_k(query, docs, embeddings, top_k=3):
    query_vec = embed_model.encode([query])  # numpy array
    scores = cosine_similarity(query_vec, embeddings)[0]  # [1, N]
    top_indices = scores.argsort()[::-1][:top_k]
    return [docs[i] for i in top_indices]

# 5. HyperCLOVA X API 호출
def call_hyperclova_x(user_query, context_docs):
    url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
    headers = {
        "Authorization": "Bearer nv-XXXXXXXXXXXXXXXXXXXXXXX",  # ✅ 실제 API 키 삽입
        "Content-Type": "application/json"
    }

    # 프롬프트 구성
    prompt = (
        f"다음은 사용자의 질문과 참고 문서입니다.\n\n"
        f"[질문]\n{user_query}\n\n"
        f"[참고 문서]\n" + "\n".join(context_docs)
    )

    # 페이로드 설정
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

    # API 호출
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["result"]["message"]["content"]
    except Exception as e:
        return f"[ERROR] HyperCLOVA API 호출 실패: {e}"
