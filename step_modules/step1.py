
import streamlit as st

def step1():
    st.markdown("### Step 1. Risk Profiling")
    st.markdown("나의 투자 성향 진단")

    options = ["생활비 확보가 필요한 자금", "1~2년 내 사용 목적 자금", "중장기 투자 목적의 여유 자금"]
    choice = st.radio("현재 투자에 사용할 수 있는 자금은 어떤 자금인가요?", options)

    if st.button("다음"):
        st.session_state.update(step=2)
    