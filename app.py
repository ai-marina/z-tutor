import streamlit as st
from PIL import Image
from rag_agent import embed_model, esg_docs, esg_embeddings, retrieve_top_k, call_hyperclova_x

# 📌 페르소나 목록 및 이미지 매핑
persona_list = ["High Risk-Return", "Low Risk", "Balanced"]

persona_image_map = {
    "High Risk-Return": "persona1.png",
    "Low Risk": "persona2.png",
    "Balanced": "persona3.png"
}

persona_prompt_map = {
    "High Risk-Return": "높은 수익을 추구하나 위험 감수 성향이 있습니다. 리스크를 감수할 수 있는 투자 상품을 중심으로 설명하세요.",
    "Low Risk": "안전성을 중요시하며 리스크가 낮은 자산을 선호합니다. 원금보존형 상품 위주로 설명하세요.",
    "Balanced": "수익과 안정성 간의 균형을 중시합니다. 포트폴리오 분산 투자 전략 중심으로 설명하세요."
}

# 🎛️ 사이드바 - 페르소나 선택
with st.sidebar:
    st.markdown("### 👤 페르소나 선택")
    persona = st.selectbox("당신의 유형은?", persona_list)
    st.markdown("선택한 유형에 따라 금융 정보 응답이 조정됩니다.")

# 🧠 메인 화면 제목
st.markdown("<h1 style='text-align: center;'>🧠 Z-Tutor: Z세대 맞춤형 금융 AI 튜터</h1>", unsafe_allow_html=True)

# 🖼️ 페르소나 이미지 출력
# 🖼️ 페르소나 이미지 출력
image_path = persona_image_map.get(persona)

if image_path:
    try:
        img = Image.open(image_path)

        # 이미지 중앙 정렬 + 크기 조절을 위한 HTML 마크업
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{base64.b64encode(img.tobytes()).decode()}" width="150"/>
                <p><b>페르소나: {persona}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    except FileNotFoundError:
        st.warning(f"이미지 파일이 존재하지 않습니다: {image_path}")

# 📥 사용자 질문 입력
st.markdown("### 💬 Z-Tutor에게 질문해보세요:")
user_input = st.text_input("예: ETF가 뭐야?", key="user_input")

# 🔁 시스템 메시지 구성
if user_input:
    with st.spinner("Z-Tutor가 답변을 작성 중입니다..."):
        system_message = f"금융 전문가로 행동하며, 대상은 '{persona}' 유형입니다. {persona_prompt_map[persona]}"
        top_docs = retrieve_top_k(user_input, esg_docs, esg_embeddings, top_k=3)
        answer = call_hyperclova_x(user_input, top_docs)
        st.markdown("#### 📌 Z-Tutor의 답변:")
        st.write(answer)
