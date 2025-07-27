
import streamlit as st

def step2():
    st.markdown("### Step 2. Goal-base Planning")
    st.markdown("나만의 투자 계획서")

    st.selectbox("예산 선택", ["500만원 이상", "1,000만원 이상", "3,000만원 이상", "5,000만원 이상", "기타"])
    st.text_input("목표 수익률 (%)")
    st.text_input("투자 기간 (년)")

    if st.button("다음"):
        st.session_state.update(step=3)
    