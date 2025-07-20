import streamlit as st
from rag_agent import embed_model, esg_docs, esg_embeddings, retrieve_top_k, call_hyperclova_x
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="Z-Tutor: Z세대 금융 로보어드바이저", layout="wide")
st.title("🧠 Z-Tutor: Z세대 맞춤형 금융 AI 튜터")

# 2. 페르소나 선택
st.sidebar.header("👤 페르소나 선택")
persona = st.sidebar.selectbox("당신의 유형은?", [
    "📱 사회 초년생", "🧾 취업 준비생", "📊 대학생 투자자", "💸 욜로족", "🧘 ESG 관심형"
])
st.sidebar.markdown("선택한 유형에 따라 금융 정보 응답이 조정됩니다.")

# 선택에 따라 이미지 표시
from PIL import Image

from PIL import Image

# 드롭다운에 사용되는 페르소나 이름 (드롭다운 value와 key 일치하게 유지)
persona_image_map = {
    "High Risk-Retune": "persona1.png",
    "Low Risk": "persona2.png",
    "Balanced": "persona3.png"
}

# 사용자 선택값
persona = st.selectbox("당신의 유형은?", list(persona_image_map.keys()))

# 이미지 표시
img_path = persona_image_map.get(persona)
if img_path:
    img = Image.open(img_path)  # main 디렉토리 기준
    st.image(img, caption=persona, use_column_width=True)
else:
    st.warning("선택한 페르소나에 대한 이미지가 없습니다.")

# 3. 질문 입력창
st.markdown("### ❓ 궁금한 금융 질문을 입력하세요")
user_query = st.text_input("예: '2030년까지 ETF 투자를 해도 괜찮을까요?'", "")

if st.button("🔍 Z-Tutor에게 질문하기") and user_query.strip():
    with st.spinner("AI 튜터가 답변 중입니다..."):

        # 1. ESG 문서에서 관련 문장 추출
        top_contexts = retrieve_top_k(user_query, esg_docs, esg_embeddings, top_k=3)
        context_text = "\n".join(top_contexts)

        # 2. 프롬프트 구성
        persona_prompt_map = {
            "High Risk-Return": "20~30대 적극적인 투자 성향을 가진 사용자로, 높은 수익을 위해 높은 리스크도 감수할 수 있습니다. ETF, 주식, 암호화폐 등에 관심이 많습니다.",
            "Low Risk": "안정성을 최우선으로 고려하는 사용자로, 원금 손실 가능성이 적은 금융상품에 관심이 있습니다. 주로 채권, 예금, 보험 등을 선호합니다.",
            "Balanced": "수익과 리스크의 균형을 중요시하는 사용자로, 포트폴리오 다변화와 장기 투자를 선호합니다. ETF, 배당주, 채권 등을 적절히 활용합니다."
        }
        
        persona = st.selectbox("당신의 투자 성향을 선택하세요:", list(persona_prompt_map.keys()))

        prompt_text = persona_prompt_map.get(persona)
        if prompt_text:
            system_message = f"당신은 '{persona}' 유형의 사용자에게 답변하는 금융 전문가입니다. 대상은 다음과 같습니다:\n{prompt_text}"
        else:
            st.error("선택한 페르소나에 대한 프롬프트 정보가 없습니다.")
            st.stop()

        # system_message = f"금융 전문가로 행동하며, 대상은 '{persona}' 유형입니다. {persona_prompt_map[persona]}"
        # prompt = f"""[ESG 정보]\n{context_text}\n\n[질문]\n{user_query}\n\n위 정보를 참고하여 답변해 주세요."""

        # 3. HyperCLOVA 호출
        response = call_hyperclova_x(prompt, system=system_message)

        # 4. 응답 출력
        st.markdown("### 🧾 Z-Tutor의 답변")
        st.markdown(response)

        with st.expander("🔎 참고한 ESG 문서 내용"):
            for i, ctx in enumerate(top_contexts):
                st.markdown(f"**{i+1}.** {ctx}")
