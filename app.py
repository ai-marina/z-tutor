import streamlit as st
from step_modules import step1, step2, step3

st.set_page_config(page_title="Z-Tutor", layout="centered")

# 현재 단계 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0

# 제목
st.markdown("## 🧠 Z세대를 위한 금융 AI: Z-Tutor")

# 단계별 화면 분기
if st.session_state.step == 0:
    # 이미지 제거하고 문구만 출력
    st.markdown("처음이라면, 나의 투자 성향부터 알아볼까요?")
    st.button("나의 투자 성향 진단하기", on_click=lambda: st.session_state.update(step=1))

elif st.session_state.step == 1:
    step1()

elif st.session_state.step == 2:
    step2()

elif st.session_state.step == 3:
    step3()
