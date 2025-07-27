import streamlit as st
from rag_agent import retrieve_top_k, call_hyperclova_x

st.set_page_config(page_title="Z-Tutor", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'risk_profile' not in st.session_state:
    st.session_state.risk_profile = {}
if 'investment_plan' not in st.session_state:
    st.session_state.investment_plan = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 Z세대를 위한 금융 AI: Z-Tutor")

# Step 0 - Intro
if st.session_state.step == 0:
    st.markdown("## 나에게 맞는 투자, 어디서부터 시작할까요?")
    if st.button("Step 1: 투자 성향 진단하기"):
        st.session_state.step = 1

# Step 1 - Risk Profiling
elif st.session_state.step == 1:
    st.markdown("## Step 1: 투자 성향 진단")
    questions = [
        "1. 현재 투자에 사용할 수 있는 자금은 어떤 자금인가요?",
        "2. 투자를 통해 어떤 목표를 기대하나요?",
        "3. 투자 경험이 있으신가요?",
        "4. 손실이 발생하면 어떻게 반응하실 건가요?",
        "5. 투자를 얼마나 오래 유지할 수 있나요?",
        "6. 투자 관련 뉴스를 얼마나 자주 보시나요?",
        "7. 가장 중요한 건 무엇이라고 생각하나요?"
    ]
    options = [
        ["생활비 일부", "여유 자금", "정기적 투자 가능한 자금"],
        ["소소한 이자 수익", "조금씩 자산 증가", "높은 수익 추구", "손실 감수 가능"],
        ["전혀 없음", "소액 간접 경험", "간접 경험 있음", "직접 경험 있음"],
        ["즉시 멈춤", "일정 손실 감수", "수익 위해 감수 가능"],
        ["6개월 이하", "1년", "2~3년", "3년 이상"],
        ["전혀 안 봄", "가끔 헤드라인", "주 2~3회", "매일"],
        ["원금 보전", "안정적 수익", "전략적 투자", "고수익/고위험"]
    ]
    for i, q in enumerate(questions):
        st.session_state.risk_profile[q] = st.radio(q, options[i], key=f"risk_{i}")

    if st.button("다음 단계로 →"):
        st.session_state.step = 2

# Step 2 - Investment Plan
elif st.session_state.step == 2:
    st.markdown("## Step 2: 투자 계획서 작성")
    st.session_state.investment_plan['예산'] = st.selectbox("1. 투자 예산은 얼마인가요?", ["500만 원 이상", "1000만 원 이상", "3000만 원 이상", "5000만 원 이상", "기타"])
    st.session_state.investment_plan['자금 출처'] = st.selectbox("2. 어떤 자금으로 투자하시나요?", ["여유 자금", "필요 시 사용", "생활비 일부 또는 대출"])
    st.session_state.investment_plan['보유 기간'] = st.selectbox("3. 투자 보유 계획", ["6개월", "1년", "2년", "기타"])
    st.session_state.investment_plan['중요 요소'] = st.radio("4. 더 중요한 것은?", ["투자 기간", "수익률"])
    st.session_state.investment_plan['희망 수익률'] = st.selectbox("5. 희망 수익률", ["20%", "40%", "70%", "100%", "기타"])
    st.session_state.investment_plan['목표 도달 시 행동'] = st.radio("목표 수익률 도달 시", ["자동 매도", "알림 받고 판단"])
    st.session_state.investment_plan['손실 시 대응'] = st.radio("6. 손실 발생 시", ["즉시 매도", "기다림", "추가 매수 고려"])
    st.session_state.investment_plan['투자 경험'] = st.multiselect("7. 투자 지식/경험", ["주식 용어 이해", "ETF 알기", "채권 잘 모름", "직접 투자 없음", "간접 투자 있음"])
    st.session_state.investment_plan['상품 관심'] = st.multiselect("8. 관심 상품", ["국내 주식", "해외 주식", "ETF", "채권", "기타"])
    st.session_state.investment_plan['투자 방식'] = st.radio("9. 투자 방식", ["일시불", "정기적", "비정기적", "모름"])
    st.session_state.investment_plan['투자 목적'] = st.selectbox("10. 투자 목적", ["자산 증식", "노후 준비", "자녀 교육", "단기 수익", "기타"])
    st.session_state.investment_plan['관심 산업'] = st.text_input("11. 관심 산업 분야 (없으면 '없음')", "")
    st.session_state.investment_plan['추천 방식'] = st.multiselect("12. 어떤 추천을 선호하시나요?", ["유명인 기반", "인기 주식 기반"])

    if st.button("포트폴리오 추천받기 →"):
        st.session_state.step = 3

# Step 3 - Portfolio + Chat
elif st.session_state.step == 3:
    st.markdown("## Step 3: 맞춤형 포트폴리오")
    st.write("🔍 당신의 투자 성향 요약:")
    for k, v in st.session_state.risk_profile.items():
        st.write(f"- {k}: {v}")
    st.write("📋 투자 계획 요약:")
    for k, v in st.session_state.investment_plan.items():
        st.write(f"- {k}: {v}")

    st.markdown("---")
    st.markdown("### 💬 Z-Tutor와의 상담")
    query = st.text_input("질문을 입력하세요", key="tutor_query")
    if query:
        with st.spinner("Z-Tutor가 답변 중입니다..."):
            profile_str = "\n".join([f"{k}:{v}" for k, v in st.session_state.risk_profile.items()])
            plan_str = "\n".join([f"{k}:{v}" for k, v in st.session_state.investment_plan.items()])
            context = f"사용자의 투자 성향 정보:\n{profile_str}\n\n사용자의 투자 계획:\n{plan_str}"
            top_docs = retrieve_top_k(query, [], [], top_k=0)
            system_msg = "너는 금융 투자 멘토야. 사용자의 성향과 계획을 고려하여 현실적이고 구체적으로 답변해."
            answer = call_hyperclova_x(user_query=query, context_docs=[context], system_message=system_msg)
            st.write(answer)
