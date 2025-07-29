# app.py (전체 구현: Step1~3 + 버튼 + API key 포함)
import streamlit as st
from rag_agent import retrieve_top_k, call_hyperclova_x
import os
import json

st.set_page_config(page_title="Z-Tutor", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'step1_data' not in st.session_state:
    st.session_state.step1_data = {}
if 'step2_data' not in st.session_state:
    st.session_state.step2_data = {}

st.title("🧠 Z세대를 위한 금융 AI: Z-Tutor")
st.divider()

# Step 1: Risk Profiling
if st.session_state.step == 1:
    st.header("Step 1. 투자 성향 진단")
    with st.form("risk_form"):
        q1 = st.radio("1. 현재 투자 자금은?", ["생활비 일부", "여유 자금", "정기적 투자 자금"])
        q2 = st.radio("2. 기대 목표는?", ["소소한 이자 수익", "안정적 자산 증가", "더 높은 수익", "고수익 감수 가능"])
        q3 = st.radio("3. 투자 경험은?", ["전혀 없음", "소액 경험 있음", "간접 투자 경험", "직접 매수·매도 경험"])
        q4 = st.radio("4. 손실 시 반응은?", ["바로 멈춤", "일정 손실 감수", "수익 위해 감수 가능"])
        q5 = st.radio("5. 투자 유지 가능 기간?", ["6개월 이하", "1년", "2~3년", "3년 이상"])
        q6 = st.radio("6. 투자 뉴스 습관은?", ["전혀 안 봄", "가끔 헤드라인", "주 2~3회", "매일 확인"])
        q7 = st.radio("7. 가장 중요한 건?", ["원금 보전", "예금 이상 수익", "전략적 수익", "고수익"])
        submitted = st.form_submit_button("진단하기")
        if submitted:
            st.session_state.step1_data = {
                "투자 자금": q1, "기대 목표": q2, "경험": q3,
                "손실 반응": q4, "투자 기간": q5, "뉴스 습관": q6, "우선 가치": q7
            }
            st.session_state.step = 2

# Step 2: Goal-based Planning
elif st.session_state.step == 2:
    st.header("Step 2. 투자 계획서 작성")
    with st.form("plan_form"):
        budget = st.radio("1. 투자 예산은?", ["5,000만 원 이상", "3,000만 원 이상", "1,000만 원 이상", "500만 원 이상", "기타"])
        fund_type = st.radio("2. 자금 종류는?", ["여유 자금", "필요 시 사용 가능 자금", "생활비 일부 또는 대출"])
        horizon = st.radio("3. 보유 계획은?", ["2년 이상", "1년 이상", "6개월 이상", "기타"])
        priority = st.radio("4. 우선순위는?", ["장기 보유", "수익 실현"])
        return_goal = st.radio("5. 수익률 목표는?", ["100% 이상", "70% 이상", "40% 이상", "20% 이상", "기타"])
        return_strategy = st.radio("수익 도달 시 전략은?", ["자동 매도", "알림 후 판단"])
        loss_strategy = st.radio("6. 손실 발생 시 대처는?", ["즉시 매도", "기다림", "추가 매수 고려"])
        know = st.multiselect("7. 투자 지식/경험?", ["주식 용어", "ETF", "채권 모름", "직접 경험 없음", "간접 투자 있음"])
        interest = st.multiselect("8. 관심 상품?", ["국내 주식", "해외 주식", "ETF", "채권"])
        method = st.radio("9. 투자 방식은?", ["일시불 투자", "정기 투자", "비정기 투자", "모름"])
        purpose = st.radio("10. 투자 목적은?", ["자산 증식", "노후 준비", "자녀 교육", "단기 수익"])
        sector = st.text_input("11. 관심 산업 분야? (없다면 추천 요청)")
        reco_style = st.multiselect("12. 추천 방식은?", ["캐시 우드 스타일", "워런 버핏 스타일", "거래량 많은 종목", "검색량 많은 산업"])
        submitted = st.form_submit_button("계획서 작성 완료")
        if submitted:
            st.session_state.step2_data = {
                "예산": budget, "자금종류": fund_type, "보유기간": horizon, "우선순위": priority,
                "목표수익률": return_goal, "수익전략": return_strategy, "손실전략": loss_strategy,
                "지식": know, "관심상품": interest, "방식": method, "목적": purpose, "산업": sector, "스타일": reco_style
            }
            st.session_state.step = 3

# Step 3: Recommend Portfolio & Chat
elif st.session_state.step == 3:
    st.header("Step 3. 포트폴리오 추천 & 챗봇")
    profile = st.session_state.step1_data
    plan = st.session_state.step2_data

    with st.expander("📝 나의 투자 계획서 요약 보기"):
        st.write("**예산:**", plan["예산"])
        st.write("**목표 수익률:**", plan["목표수익률"])
        st.write("**투자 기간:**", plan["보유기간"])
        st.write("**관심 산업:**", plan["산업"])
        st.write("**투자 스타일:**", ", ".join(plan["스타일"]) if plan["스타일"] else "없음")

    st.subheader("📊 추천 포트폴리오")
    if profile["우선 가치"] in ["원금 보전", "안정적 자산 증가"]:
        st.info("당신은 '안정형'입니다. → 채권 ETF + 배당 우량주")
    elif profile["우선 가치"] in ["전략적 수익"]:
        st.info("당신은 '중립형'입니다. → ETF + 우량 성장주")
    else:
        st.info("당신은 '공격형'입니다. → 레버리지 ETF + 성장 테마주")

    st.divider()
    st.subheader("💬 Z-Tutor에게 질문해 보세요")
    user_input = st.text_input("질문을 입력하세요")
    if user_input:
        context_docs = retrieve_top_k(user_input)
        persona_context = f"[사용자 성향] {json.dumps(profile, ensure_ascii=False)}\n[사용자 계획] {json.dumps(plan, ensure_ascii=False)}"
        system_message = f"너는 금융 AI 튜터야. 아래 사용자 정보와 관련 문서를 참고해 정확하고 신뢰할 수 있는 답변을 생성해.\n{persona_context}"
        answer = call_hyperclova_x(user_query=user_input, context_docs=context_docs, system_message=system_message)
        st.success(answer)

    # 버튼
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🔚 대화 종료"):
        st.session_state.step = 0
    if col2.button("🔁 진단하기로 돌아가기"):
        st.session_state.step = 1
    if col3.button("📄 계획서로 돌아가기"):
        st.session_state.step = 2
    if col4.button("📊 대시보드 확인하기"):
        st.info("🚧 대시보드 기능은 구현 예정입니다. (향후 확장 가능)")
