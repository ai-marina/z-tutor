# 💰 Z-Tutor: HyperCLOVA X 기반 Z세대 맞춤형 금융 튜터

미래에셋 AI Festival 출품작  
Z세대 투자자를 위한 퍼스널 금융 AI 에이전트  

---

## 📑 제출 자료 리스트

| 📂 항목         | 🔗 내용                                                                                               |
|----------------|--------------------------------------------------------------------------------------------------------|
| 🗣️ 발표 자료     | [Z-Tutor_제안서.pptx 또는 PDF](https://github.com/ai-marina/z-tutor/blob/main/1.%20%5B%EB%B3%B8%EB%B3%B4%EA%B3%A0%EC%84%9C%5D%20%EC%9E%84%EB%B0%95%27s%20Tutor_%EC%9E%84%EC%A7%80%EC%84%A0_Z%EC%84%B8%EB%8C%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20Tutor_Z-Tutor.pdf) |
| 🛠️ 서비스 소스코드 | [Github 저장소 (RAG + API 연동)](https://github.com/ai-marina/z-tutor)                                      |
| 🌐 Streamlit 데모 | [Z-Tutor 시연용 페이지](https://z-tutor.streamlit.app/)                                                   |

---

## 🧠 서비스 개요

**Z-Tutor**는 HyperCLOVA X 기반의 금융 문해력 튜터로서, Z세대의 투자 성향과 재무계획을 바탕으로 맞춤형 자산 포트폴리오 추천 및 ESG 투자 뉴스 큐레이션을 제공합니다.

- **Step1**: 개인 투자 성향 진단 (투자 목적, 리스크 감수 성향, 투자 기간 등)
- **Step2**: 투자 계획 입력 (금액, 주기, 선호 업종 등)
- **Step3**: 포트폴리오 및 ESG 뉴스 기반 투자 제안
- **Step4**: 챗봇 기반 금융 상담

---

## 🧩 기술 구성도

```plaintext
[User Input]
     ↓
[Investment Profile & Plan] → [Prompt 구성]
     ↓
[RAG 기반 ESG 정보 검색]
     ↓
[HyperCLOVA X HCX-005 API 호출]
     ↓
[맞춤형 금융 조언 및 ETF 추천 생성]


