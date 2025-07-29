import streamlit as st
from rag_agent import retrieve_top_k, call_hyperclova_x

st.set_page_config(page_title="Z-Tutor", layout="wide")

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'risk_profile' not in st.session_state:
    st.session_state.risk_profile = {}
if 'investment_plan' not in st.session_state:
    st.session_state.investment_plan = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Step1. 투자 성향 진단
def step1():
    st.header("STEP 1. 투자 성향 진단 (Risk Profiling)")

    questions = {
        "자금 성격": st.radio("1. 현재 투자 자금은?", ["생활비 일부", "여유 자금", "정기적으로 투자 가능한 자금"]),
        "투자 목표": st.radio("2. 투자 목표는?", ["손실 없이 이자 수익", "안정적 자산 증가", "높은 수익", "고수익 감수"]),
        "경험": st.radio("3. 투자 경험은?", ["전혀 없음", "펀드/주식 경험 있음", "간접 경험 있음", "매수·매도 해봄"]),
        "손실 대응": st.radio("4. 손실 발생 시?", ["즉시 멈춤", "일정 손실 감수", "수익 기대하고 감수"]),
        "투자 기간": st.radio("5. 투자 기간?", ["6개월 이하", "1년", "2~3년", "3년 이상"]),
        "뉴스 습관": st.radio("6. 투자 뉴스 확인 빈도?", ["전혀 안 봄", "가끔 헤드라인", "주 2~3회", "거의 매일"]),
        "우선순위": st.radio("7. 투자 시 가장 중요한 것은?", ["원금 보전", "안정적 수익", "전략적 투자", "고수익"])
    }

    if st.button("진단하기"):
        st.session_state.risk_profile = questions
        st.session_state.step = 2

# Step2. 투자 계획
def step2():
    st.header("STEP 2. 투자 계획서 작성 (Goal-based Planning)")

    col1, col2 = st.columns(2)
    with col1:
        budget = st.radio("1. 투자 예산은?", ["500만 원 이상", "1,000만 원 이상", "3,000만 원 이상", "5,000만 원 이상", "기타"])
        purpose = st.radio("2. 어떤 자금으로 투자?", ["여유 자금", "꺼낼 수 있는 자금", "생활비/긴급 자금"])
        period = st.radio("3. 투자 보유 기간은?", ["6개월 이상", "1년 이상", "2년 이상", "기타"])
        goal = st.radio("4. 투자 시 더 중시하는 것은?", ["투자 기간", "수익률"])

    with col2:
        target_return = st.radio("5. 희망 수익률은?", ["20%", "40%", "70%", "100%", "기타"])
        action = st.radio("목표 수익률 도달 시 대응은?", ["자동 매도", "알림 후 판단"])
        loss_response = st.radio("6. 손실 발생 시?", ["즉시 매도", "기다림", "추가 매수"])
        knowledge = st.multiselect("7. 투자 지식/경험", ["주식 용어", "ETF", "채권", "직접 경험 없음", "간접 투자 경험"])

    product_interest = st.multiselect("8. 관심 상품", ["국내 주식", "해외 주식", "ETF", "채권"])
    strategy = st.radio("9. 투자 방식", ["일시불", "정기 투자", "비정기", "모름"])
    reason = st.radio("10. 주요 투자 목적", ["자산 증식", "노후 준비", "교육 자금", "단기 수익", "기타"])
    industry = st.text_input("11. 관심 산업 분야", "성장 산업")
    style = st.multiselect("12. 선호 추천 방식", ["유명인 스타일", "인기 종목 중심"])

    if st.button("계획서 생성하기"):
        st.session_state.investment_plan = {
            "예산": budget,
            "자금 성격": purpose,
            "기간": period,
            "수익률 목표": target_return,
            "수익률 도달시": action,
            "손실 대응": loss_response,
            "지식": knowledge,
            "관심 상품": product_interest,
            "방식": strategy,
            "목적": reason,
            "산업": industry,
            "스타일": style
        }
        st.session_state.step = 3

# Step3. 포트폴리오 제안 + 챗봇
def step3():
    st.header("STEP 3. 맞춤형 포트폴리오 및 상담")

    risk = st.session_state.risk_profile.get("자금 성격", "")
    rec = "ETF + 우량주" if "여유" in risk else "채권 ETF + 배당주"
    st.subheader(f"🎯 당신은 '{risk}' 투자자입니다. 추천: {rec}")

    st.divider()
    user_input = st.text_input("Z-Tutor에게 질문해 보세요.")
    if st.button("질문하기") and user_input:
        prompt_context = f"""[고객 성향]
투자 성향: {st.session_state.risk_profile}
투자 계획: {st.session_state.investment_plan}

[고객 질문]
{user_input}"""
        top_docs = retrieve_top_k(user_input, k=3)
        response = call_hyperclova_x(user_input, top_docs, prompt_context)
        st.session_state.chat_history.append((user_input, response))

    for q, a in st.session_state.chat_history[::-1]:
        st.markdown(f"**🙋 사용자 질문:** {q}")
        st.markdown(f"**🤖 Z-Tutor 답변:** {a}")
        st.divider()

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("대화 종료"):
        st.session_state.step = 3
        st.session_state.chat_history = []
    if col2.button("진단하기로 돌아가기"):
        st.session_state.step = 1
    if col3.button("계획서로 돌아가기"):
        st.session_state.step = 2
    if col4.button("대시보드 확인하기"):
        st.session_state.step = 4

# Step4. 간단한 대시보드
def dashboard():
    st.header("📊 투자자 요약 대시보드")
    st.write("### 투자 성향 진단 결과")
    st.json(st.session_state.risk_profile)
    st.write("### 투자 계획서 요약")
    st.json(st.session_state.investment_plan)

    if st.button("처음으로"):
        st.session_state.step = 1

# 라우팅
if st.session_state.step == 1:
    step1()
elif st.session_state.step == 2:
    step2()
elif st.session_state.step == 3:
    step3()
elif st.session_state.step == 4:
    dashboard()
