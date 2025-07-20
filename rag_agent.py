import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# 1. Load data (한글 인코딩 고려 + 경로 반영)
etf_df = pd.read_csv("data_4908_20250720.csv", encoding='cp949')

# 2. 검색용 문장 생성 (존재하는 컬럼 조합: 종목명 + 기초지수명)
etf_df["esg_text"] = etf_df["종목명"] + "는 " + etf_df["기초지수_지수명"] + " 지수를 추종합니다."

# 3. 임베딩 모델 로딩
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 4. 문장 임베딩 벡터화
esg_docs = etf_df["esg_text"].tolist()
esg_embeddings = embed_model.encode(esg_docs)

# 5. 유사도 기반 검색 함수
def retrieve_top_k(query, docs, embeddings, top_k=3):
    query_vec = embed_model.encode([query])
    scores = cosine_similarity(query_vec, embeddings)[0]
    top_indices = scores.argsort()[::-1][:top_k]
    return [docs[i] for i in top_indices]

# 6. HyperCLOVA X 호출 함수
def call_hyperclova_x(user_query, context_docs):
    url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
    headers = {
        "Authorization": "Bearer nv-50bf48a41b1848c09b1c77f84d75cd5bsZTj",  # 🔁 여기에 본인의 API 키 입력
        "Content-Type": "application/json"
    }
    prompt = (
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
