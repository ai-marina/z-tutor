
import streamlit as st

def step3():
    st.markdown("### Step 3. Personalized Portfolio")
    st.markdown("나만의 포트폴리오")

    st.write("분석된 투자 성향에 따라 아래와 같이 추천됩니다.")
    st.success("안정형: 채권형 ETF + 배당 우량주")
    st.info("중립형: ETF 중심 + 일부 성장주")
    st.error("공격형: 테마주 + 글로벌 기술주 + 레버리지 일부")

    st.button("Z-Tutor 상담")
    