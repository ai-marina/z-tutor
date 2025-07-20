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
persona_image_map = {
    "📱 사회 초년생": "persona1.png",
    "🧾 취업 준비생": "persona2.png",
    "📊 대학생 투자자": "persona3.png",
    "💸 욜로족": "persona4.png",
    "🧘 ESG 관심형": "persona5.png"
}
img = Image.open(f"persona_images/{persona_image_map[persona]}")
st.sidebar.image(img, caption=persona, use_column_width=True)

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
            "📱 사회 초년생": "경제에 입문한 사회 초년생에게 설명하듯 쉽게 설명해 주세요.",
            "🧾 취업 준비생": "재무 지식이 없는 취준생을 위한 설명을 제공해 주세요.",
            "📊 대학생 투자자": "대학생 투자자가 이해할 수 있도록 분석 기반으로 설명해 주세요.",
            "💸 욜로족": "간결하고 실용적인 투자 조언 중심으로 설명해 주세요.",
            "🧘 ESG 관심형": "ESG 관점에서 친환경·윤리적 투자 측면을 고려해 설명해 주세요."
        }

        system_message = f"금융 전문가로 행동하며, 대상은 '{persona}' 유형입니다. {persona_prompt_map[persona]}"
        prompt = f"""[ESG 정보]\n{context_text}\n\n[질문]\n{user_query}\n\n위 정보를 참고하여 답변해 주세요."""

        # 3. HyperCLOVA 호출
        response = call_hyperclova_x(prompt, system=system_message)

        # 4. 응답 출력
        st.markdown("### 🧾 Z-Tutor의 답변")
        st.markdown(response)

        with st.expander("🔎 참고한 ESG 문서 내용"):
            for i, ctx in enumerate(top_contexts):
                st.markdown(f"**{i+1}.** {ctx}")
