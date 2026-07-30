import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="MBTI 일본 여행지 추천",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #FFF5F9 0%, #FFE4F0 100%);
    }
    .stButton > button {
        background-color: #FFB6D9;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF9DC5;
    }
    h1, h2, h3 {
        color: #D4526E;
        font-weight: bold;
    }
    .result-box {
        background-color: #FFEEF7;
        border: 2px solid #FFB6D9;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 여행지 데이터
travel_data = {
    "ISTJ": {
        "name": "현실적인 계획가",
        "location": "도쿄 & 교토",
        "description": "효율적이고 체계적인 여행을 즐기는 당신을 위한 추천입니다.",
        "spots": ["도쿄 국립박물관", "교토 기온", "아라시야마 대나무숲"],
        "budget": "2,500,000원",
        "duration": "7일"
    },
    "ISFJ": {
        "name": "따뜻한 관찰자",
        "location": "오사카 & 나라",
        "description": "사람의 온기가 담긴 전통적인 경험을 추천합니다.",
        "spots": ["오사카 성", "나라 공원", "톤다바야시 마을"],
        "budget": "2,000,000원",
        "duration": "5일"
    },
    "INFJ": {
        "name": "신비로운 선지자",
        "location": "교토 & 시라카와고",
        "description": "정신적인 깊이와 아름다움을 느낄 수 있는 여행지입니다.",
        "spots": ["키요미즈데라", "시라카와고 마을", "철학의 길"],
        "budget": "2,800,000원",
        "duration": "6일"
    },
    "INTJ": {
        "name": "독립적인 전략가",
        "location": "도쿄 & 오키나와",
        "description": "독특한 관점으로 여행을 즐기는 당신을 위한 특별한 경험입니다.",
        "spots": ["팀버튼 미술관", "오키나와 해양박물관", "신주쿠 야경"],
        "budget": "3,000,000원",
        "duration": "8일"
    },
    "ISTP": {
        "name": "논리적인 장인",
        "location": "아키하바라 & 도쿄",
        "description": "기술과 혁신을 체험할 수 있는 여행입니다.",
        "spots": ["teamLab Borderless", "아키하바라 전자상가", "로봇 레스토랑"],
        "budget": "2,200,000원",
        "duration": "4일"
    },
    "ISFP": {
        "name": "예술적인 모험가",
        "location": "도쿄 & 가나자와",
        "description": "미적 감각과 자유로운 경험을 선사합니다.",
        "spots": ["21세기 미술관", "하이쿠 박물관", "오모테산도 거리"],
        "budget": "2,400,000원",
        "duration": "6일"
    },
    "INFP": {
        "name": "이상주의자 중재자",
        "location": "교토 & 다카야마",
        "description": "감정과 영감이 넘치는 낭만적인 여행입니다.",
        "spots": ["마지막 사무라이 촬영지", "향림사", "오사카 야경"],
        "budget": "2,600,000원",
        "duration": "7일"
    },
    "INTP": {
        "name": "지식을 탐구하는 철학자",
        "location": "도쿄 & 교토",
        "description": "역사와 문화의 깊이를 탐구하는 여행입니다.",
        "spots": ["도쿄 대학 캠퍼스", "교토 철학의 길", "일본 근현대 미술관"],
        "budget": "2,300,000원",
        "duration": "6일"
    },
    "ESTP": {
        "name": "모험을 즐기는 사업가",
        "location": "후쿠오카 & 나고야",
        "description": "짜릿한 경험과 즉흥적인 모험으로 가득합니다.",
        "spots": ["야타이 음식거리", "스카이 번지점프", "토요타 박물관"],
        "budget": "2,100,000원",
        "duration": "4일"
    },
    "ESFP": {
        "name": "즐거움의 연예인",
        "location": "도쿄 & 오사카",
        "description": "재미있고 활기찬 경험들로 가득한 여행입니다.",
        "spots": ["도쿄 디즈니랜드", "오사카 도톤보리", "일본 축제"],
        "budget": "2,700,000원",
        "duration": "5일"
    },
    "ENFP": {
        "name": "열정적인 캠페이너",
        "location": "도쿄 & 오사카 & 교토",
        "description": "새로운 만남과 경험이 가득한 여행입니다.",
        "spots": ["하라주쿠", "도톤보리", "철학의 길"],
        "budget": "3,000,000원",
        "duration": "7일"
    },
    "ENTP": {
        "name": "진취적인 변론가",
        "location": "도쿄 & 오키나와",
        "description": "논의와 발견으로 가득한 지적 모험입니다.",
        "spots": ["teamLab", "오키나와 문화 박물관", "신쥬쿠 야경"],
        "budget": "2,900,000원",
        "duration": "7일"
    },
    "ESTJ": {
        "name": "엄격한 관리자",
        "location": "도쿄 & 오사카",
        "description": "효율적이고 체계적인 일정으로 도시를 정복합니다.",
        "spots": ["도쿄 역", "오사카 성", "신칸센 체험"],
        "budget": "2,000,000원",
        "duration": "5일"
    },
    "ESFJ": {
        "name": "사교적인 영사",
        "location": "교토 & 오사카",
        "description": "따뜻한 인정과 함께하는 여행입니다.",
        "spots": ["기요미즈데라", "도톤보리 음식투어", "마지코 거리"],
        "budget": "2,200,000원",
        "duration": "5일"
    },
    "ENFJ": {
        "name": "카리스마 있는 리더",
        "location": "도쿄 & 교토 & 오사카",
        "description": "영감과 감동이 넘치는 여행을 주도합니다.",
        "spots": ["센소지 사원", "히라유 온천", "교토 야경"],
        "budget": "2,800,000원",
        "duration": "7일"
    },
    "ENTJ": {
        "name": "전략적인 사령관",
        "location": "도쿄 & 싱가포르",
        "description": "비전과 전략으로 여행을 완벽하게 계획합니다.",
        "spots": ["도쿄 메트로폴리탄", "오다이바", "로봇 레스토랑"],
        "budget": "3,200,000원",
        "duration": "8일"
    }
}

# 페이지 네비게이션
with st.sidebar:
    selected = option_menu(
        "📍 일본 여행 추천",
        ["🏠 홈", "🧪 MBTI 진단", "🗺️ 추천지", "💬 문의"],
        icons=["house", "clipboard", "map", "chat"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#FFE4F0"},
            "icon": {"color": "#FFB6D9", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "10px"},
            "nav-link-selected": {"background-color": "#FFB6D9"},
        }
    )

# 페이지 1: 홈
if selected == "🏠 홈":
    st.markdown("<h1 style='text-align: center;'>🌸 MBTI로 찾는 일본 여행지 🌸</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://images.unsplash.com/photo-1540959375944-7049f642e9c5?w=400", use_column_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1522383750931-11fce5dbc3f6?w=400", use_column_width=True)
    with col3:
        st.image("https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=400", use_column_width=True)
    
    st.markdown("""
    <div class='result-box'>
    <h3>🎌 당신의 성격 유형에 맞는 일본 여행지를 추천해드립니다!</h3>
    
    **MBTI 진단**을 통해 당신의 성격 유형을 파악하고,
    그에 맞는 일본의 숨은 보석 같은 여행지들을 만나보세요.
    
    - 🗺️ 개인 맞춤형 여행지 추천
    - 💰 예산 정보 및 일정 제안
    - 🎯 성격에 맞는 관광지 정보
    </div>
    """, unsafe_allow_html=True)

# 페이지 2: MBTI 진단
elif selected == "🧪 MBTI 진단":
    st.markdown("<h2>당신의 MBTI를 선택하세요</h2>", unsafe_allow_html=True)
    
    mbti_type = st.selectbox(
        "MBTI 선택:",
        ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
         "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
    )
    
    if st.button("추천 받기 🎁", use_container_width=True):
        st.session_state.selected_mbti = mbti_type
        st.switch_page("pages/recommendation.py") if False else None
        st.success(f"✅ {mbti_type} 타입의 추천을 보여드립니다!")
        
        info = travel_data[mbti_type]
        
        st.markdown(f"""
        <div class='result-box'>
        <h3>{info['name']}</h3>
        <p><strong>추천 여행지:</strong> {info['location']}</p>
        <p><strong>설명:</strong> {info['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🏮 추천 관광지")
        for spot in info['spots']:
            st.markdown(f"✨ {spot}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 예상 예산", info['budget'])
        with col2:
            st.metric("📅 추천 일정", info['duration'])

# 페이지 3: 추천지
elif selected == "🗺️ 추천지":
    st.markdown("<h2>MBTI별 여행지 가이드</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs(["E", "I"])
    
    with tabs[0]:
        st.subheader("외향형 (Extrovert)")
        col
