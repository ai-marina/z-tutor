import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
import requests

# 1. ESG 데이터 로딩
def load_esg_data(csv_path):
    df = pd.read_csv(csv_path)
    return df['content'].tolist() if 'content' in df.columns else df.iloc[:, 0].tolist()

# 2. 임베딩 모델 초기화 및 문서 임베딩 생성
def create_embeddings(docs, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(docs, convert_to_tensor=True, show_progress_bar=True)
    return model, embeddings

# 3. 질의에 대해 유사한 문장 top-k 반환
def retrieve_top_k(query, docs, embeddings, model, top_k=3):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_results = torch.topk(scores, k=top_k)
    return [docs[idx] for idx in top_results[1]]

# 4. HyperCLOVA X API 호출
def call_hyperclova_x(prompt):
    url = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"
    headers = {
        "Authorization": "Bearer nv-50bf48a41b1848c09b1c77f84d75cd5bsZTj",  # 본인의 API 키
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "너는 친절한 금융 어드바이저야. 초보자 눈높이에 맞게 설명해줘."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "topP": 0.8,
        "maxTokens": 1024,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["result"]["message"]["content"]
    except Exception as e:
        return f"[ERROR] HCX API 호출 실패: {e}"

# 5. 전체 RAG 파이프라인
def rag_response(user_query, docs, embeddings, model):
    relevant_contexts = retrieve_top_k(user_query, docs, embeddings, model)
    context_str = "\n".join(f"- {ctx}" for ctx in relevant_contexts)
    prompt = f"다음은 ESG 관련 문서야:\n{context_str}\n\n위 내용을 참고해서 아래 질문에 답해줘:\n{user_query}"
    return call_hyperclova_x(prompt)
