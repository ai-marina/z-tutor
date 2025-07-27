import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import requests

# ------------------ 0. HCX API 설정 ------------------
HCX_API_URL = "https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-005"  # 실제 엔드포인트 입력
HCX_API_KEY = "Bearer nv-50bf48a41b1848c09b1c77f84d75cd5bsZTj"  # 보안 고려하여 환경변수로 대체 권장
MODEL_NAME = "HCX-005"

# ------------------ 1. 문서 임베딩 RAG 준비 ------------------
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
document_texts = [
    "ETF란 상장지수펀드로, 특정 지수를 추종하는 상품입니다.",
    "적립식 투자는 일정 금액을 주기적으로 투자하는 방식입니다.",
    "목표 수익률은 투자자의 성향과 시장 상황에 따라 설정됩니다.",
    "국내 ETF는 코스피, 코스닥을 추종하며 안정적인 수익을 추구합니다.",
    "해외 ETF는 S&P500, 나스닥 등의 지수를 추종하며 다양한 산업에 투자합니다.",
    "채권형 ETF는 변동성이 낮고 안정적인 수익을 추구합니다."
]
document_embeddings = embedding_model.encode(document_texts, convert_to_numpy=True)
document_index = faiss.IndexFlatL2(document_embeddings.shape[1])
document_index.add(document_embeddings)

# ------------------ 2. 함수 정의 ------------------
def retrieve_top_k(query: str, top_k: int = 3):
    if not query or top_k <= 0:
        return []
    query_vec = embedding_model.encode([query], convert_to_numpy=True)
    _, indices = document_index.search(query_vec, top_k)
    return [document_texts[i] for i in indices[0]]

def construct_prompt(user_profile: str, context_docs: list, user_query: str) -> str:
    context = "\n".join(context_docs)
    return f"""
당신은 Z세대를 위한 친절한 금융 튜터입니다.

[사용자 정보]
{user_profile}

[문맥 정보]
{context}

[사용자 질문]
{user_query}

위 정보를 바탕으로 현실적이고 명확하게 투자 조언을 제공하세요.
"""

def call_hyperclova_x(user_query: str, context_docs: list, user_profile: str):
    prompt = construct_prompt(user_profile, context_docs, user_query)
    headers = {
        "X-NCP-CLOVASTUDIO-API-KEY": HCX_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    response = requests.post(HCX_API_URL, headers=headers, json=payload)
    return response.json()['result']['message']['content']

# ------------------ 3. Streamlit UI 구성 ------------------
st.set_page_config(page_title="Z-Tutor", layout="centered")
st.title("🧠 Z세대 금융 어드바이저: Z-Tutor")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'profile_answers' not in st.session_state:
    st.session_state.profile_answers = {}
if 'plan_answers' not in st.session_state:
    st.session_state.plan_answers = {}

# ------------------ Step 1: 투자 성향 ------------------
if st.session_state.step == 1:
    st.header("Step 1. 투자 성향 진단")
    profile_questions = [
        ("성별", ["남성", "여성", "기타"]),
        ("나이", ["10대", "20대", "30대", "40대 이상"]),
        ("직업군", ["학생", "직장인", "프리랜서", "무직"]),
        ("월 투자 가능 금액", ["10만 원 미만", "10~50만 원", "50~100만 원", "100만 원 이상"]),
        ("투자 경험", ["없음", "1년 이하", "1~3년", "3년 이상"]),
        ("선호 투자 상품", ["ETF", "채권", "주식", "암호화폐"]),
        ("위험 선호도", ["고위험", "중위험", "저위험"]),
    ]

    for q, options in profile_questions:
        st.session_state.profile_answers[q] = st.radio(q, options, key=q)

    if st.button("다음으로", type="primary"):
        st.session_state.step = 2

# ------------------ Step 2: 투자 계획 ------------------
elif st.session_state.step == 2:
    st.header("Step 2. 투자 목표 및 계획")
    plan_questions = [
        "당신의 투자 목표는 무엇인가요?",
        "목표 금액은 얼마인가요?",
        "목표 수익률은 몇 %인가요?",
        "목표 달성까지 예상 기간은?",
        "예상 투자 빈도는?",
        "투자 관심 산업군은?",
        "선호하는 투자 지역은?",
        "투자 시 중요하게 생각하는 요소는?",
        "포트폴리오 구성 시 선호하는 전략은?",
        "투자에 대한 우려 또는 고민은?",
        "과거에 했던 투자 실수나 배운 점은?",
        "추가적으로 전달하고 싶은 정보는?"
    ]
    for q in plan_questions:
        st.session_state.plan_answers[q] = st.text_input(q, key=q)

    if st.button("내 포트폴리오 추천받기", type="primary"):
        st.session_state.step = 3

# ------------------ Step 3: 포트폴리오 추천 및 튜터링 ------------------
elif st.session_state.step == 3:
    st.header("Step 3. 나만의 포트폴리오")

    persona_summary = "\n".join([
        f"{k}: {v}" for k, v in st.session_state.profile_answers.items()
    ]) + "\n" + "\n".join([
        f"{k}: {v}" for k, v in st.session_state.plan_answers.items()
    ])

    st.markdown(f"**당신의 투자 프로필:**\n\n{persona_summary}")

    user_input = st.text_input("Z-Tutor에게 질문해보세요!", key="tutor_input")
    if st.button("상담 시작") and user_input:
        top_docs = retrieve_top_k(user_input)
        answer = call_hyperclova_x(user_query=user_input, context_docs=top_docs, user_profile=persona_summary)
        st.markdown(f"#### 💬 Z-Tutor의 답변\n{answer}")
