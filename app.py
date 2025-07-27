# app.py
import streamlit as st
from rag_agent import retrieve_top_k, call_hyperclova_x

st.set_page_config(page_title="Z-Tutor", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'step1_data' not in st.session_state:
    st.session_state.step1_data = {}
if 'step2_data' not in st.session_state:
    st.session_state.step2_data = {}

st.title("🧠 Z세대를 위한 금융 AI: Z-Tutor")
st.divider()

if st.session_state.step == 1:
    st.header("Step 1. 나의 투자 성향 진단")

    st.session_state.step1_data['투자 목적'] = st.radio("1. 당신의 주요 투자 목적은 무엇인가요?", ["단기 수익", "장기 자산 형성", "은퇴 준비", "기타"])
    st.session_state.step1_data['리스크 감수 성향'] = st.radio("2. 손실 가능성이 있더라도 높은 수익을 추구하시나요?", ["예", "아니오"])
    st.session_state.step1_data['투자 경험'] = st.radio("3. 투자 경험이 얼마나 되셨나요?", ["없음", "1~3년", "3년 이상"])
    st.session_state.step1_data['선호 자산 유형'] = st.multiselect("4. 선호하는 투자 자산을 선택하세요", ["주식", "채권", "ETF", "부동산", "암호화폐"])

    if st.button("다음으로", type="primary"):
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.header("Step 2. 투자 계획서 작성")
    st.session_state.step2_data['목표 금액'] = st.radio("1. 투자 목표 금액은 얼마인가요?", ["500만원 이하", "500만~2000만원", "2000만원 이상"])
    st.session_state.step2_data['투자 기간'] = st.radio("2. 투자 가능 기간은 얼마나 되시나요?", ["1년 이하", "1~3년", "3년 이상"])
    st.session_state.step2_data['투자 빈도'] = st.radio("3. 자산을 얼마나 자주 점검하고 조정하나요?", ["주 1회 이상", "월 1회", "거의 안함"])

    if st.button("포트폴리오 추천 받기", type="primary"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.header("Step 3. 포트폴리오 추천 및 Z-Tutor 상담")
    user_input = st.text_input("Z-Tutor에게 궁금한 점을 입력하세요", placeholder="예: ETF란 무엇인가요?")

    if user_input:
        with st.spinner("Z-Tutor가 답변 중입니다..."):
            # 사용자 정보 요약
            profile_summary = "\n".join([
                f"{k}: {v}" for k, v in st.session_state.step1_data.items()
            ] + [
                f"{k}: {v}" for k, v in st.session_state.step2_data.items()
            ])

            system_msg = f"당신은 금융 상담 전문가이며, 다음 사용자 정보를 고려하여 조언합니다:\n{profile_summary}"
            context = retrieve_top_k(user_input)
            try:
                answer = call_hyperclova_x(user_query=user_input, context_docs=context, system_message=system_msg)
                st.success("Z-Tutor의 답변:")
                st.write(answer)
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
