import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="🌸 일본여행 MBTI 추천",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 (핑크톤)
st.markdown("""
    <style>
    :root {
        --primary-color: #FFB6D9;
        --secondary-color: #FFC0CB;
        --tertiary-color: #FFE4F0;
    }
    
    * {
        color: #333333;
    }
    
    [data-testid="stHeader"] {
        background-color: #FFB6D9 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFE4F0 !important;
    }
    
    .main {
        background-color: #FFF5F9 !important;
    }
    
    h1, h2, h3 {
        color: #C2185B !important;
        font-weight: 700;
    }
    
    .stButton > button {
        background-color: #FFB6D9 !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #FF69B4 !important;
        transform: scale(1.05) !important;
    }
    
    .result-box {
        background: linear-gradient(135deg, #FFB6D9 0%, #FFC0CB 100%) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.2) !important;
        margin: 20px 0 !important;
    }
    
    .destination-card {
        background-color: white !important;
        border-left: 5px solid #FFB6D9 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin: 15px 0 !important;
        box-shadow: 0 2px 10px rgba(255, 182, 217, 0.1) !important;
    }
    
    .stSelectbox, .stRadio {
        background-color: white !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #FFE4F0 !important;
        color: #C2185B !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFB6D9 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 정의
MBTI_DESTINATIONS = {
    "ENFP": {
        "name": "자유로운 모험가",
        "destinations": [
            {
                "place": "🌃 도쿄 (도심 탐방)",
                "description": "에너지 넘치는 활기찬 분위기의 시부야, 신주쿠, 하라주쿠 거리 탐방",
                "attractions": ["팀버튼 카페", "메이드 카페", "로봇 레스토랑", "오다이바"],
                "duration": "3-4일",
                "budget": "중상"
            },
            {
                "place": "🎪 오사카 (자유로운 분위기)",
                "description": "도톤보리의 활기찬 야시장과 문화 공간",
                "attractions": ["도톤보리", "오사카성", "흥겐지 사원", "유니버셜 스튜디오"],
                "duration": "2-3일",
                "budget": "중상"
            },
            {
                "place": "🏯 교토 (역사와 현대의 조화)",
                "description": "전통과 현대가 만나는 신사 탐방 및 체험 활동",
                "attractions": ["마치야 카페", "게이샤 공연", "기온 지구", "대나무숲"],
                "duration": "2-3일",
                "budget": "중상"
            }
        ]
    },
    "ENFJ": {
        "name": "따뜻한 리더",
        "destinations": [
            {
                "place": "❤️ 교토 (전통 문화)",
                "description": "사람들과 연결되는 문화체험과 전통 공예 활동",
                "attractions": ["게이샤 공연", "다도 체험", "기모노 입기", "사찰 투숙"],
                "duration": "3-4일",
                "budget": "중상"
            },
            {
                "place": "🏮 오사카 (사람과의 만남)",
                "description": "현지인과의 만남과 공동체 분위기의 장소들",
                "attractions": ["로컬 야시장", "온천마을", "오사카 축제", "호텔 브레이크패스트"],
                "duration": "2-3일",
                "budget": "중상"
            },
            {
                "place": "🌸 아라시야마 (예술과 영감)",
                "description": "예술가적 영감을 주는 자연과 전시관",
                "attractions": ["대나무숲", "메종 드 프뢰유르", "미술관", "예술 카페"],
                "duration": "1-2일",
                "budget": "중상"
            }
        ]
    },
    "INFP": {
        "name": "몽상가 예술가",
        "destinations": [
            {
                "place": "🌸 아라시야마 (영감의 공간)",
                "description": "조용하고 영감을 주는 자연 속의 예술 공간",
                "attractions": ["대나무숲", "료안지 정원", "미술관", "예술 카페"],
                "duration": "2-3일",
                "budget": "중하"
            },
            {
                "place": "🏯 쿠릴시마 (섬의 고요함)",
                "description": "독립적인 예술가들의 섬에서의 조용한 시간",
                "attractions": ["미술관", "아티스트 스튜디오", "해변 산책", "갤러리"],
                "duration": "2-3일",
                "budget": "중하"
            },
            {
                "place": "📚 가나자와 (문화 도시)",
                "description": "조용하고 감성적인 전통 도시",
                "attractions": ["미술관", "정원", "게이샤 구역", "전통공예 체험"],
                "duration": "2일",
                "budget": "중하"
            }
        ]
    },
    "INFJ": {
        "name": "통찰하는 현자",
        "destinations": [
            {
                "place": "🏛️ 교토 (영적 통찰)",
                "description": "깊은 명상과 영적 체험을 할 수 있는 사찰들",
                "attractions": ["금각사", "은각사", "사찰 명상", "선학원"],
                "duration": "3-4일",
                "budget": "중상"
            },
            {
                "place": "🏔️ 후지산 지역 (자연과 명상)",
                "description": "조용한 자연 속에서의 영적 재충전",
                "attractions": ["후지산 등반", "호수 산책", "온천", "숲 명상"],
                "duration": "3일",
                "budget": "중상"
            },
            {
                "place": "🌿 다카야마 (산촌 체험)",
                "description": "전통 마을에서의 느린 여행",
                "attractions": ["전통 마을", "사찰 숙박", "자연 산책", "공예 체험"],
                "duration": "2-3일",
                "budget": "중하"
            }
        ]
    },
    "ENTJ": {
        "name": "전략적 지휘관",
        "destinations": [
            {
                "place": "💼 도쿄 (비즈니스 지구)",
                "description": "일본의 경제 중심지와 최신 기술 체험",
                "attractions": ["도쿄 증권거래소", "가제호시 신사", "기술박물관", "고급 레스토랑"],
                "duration": "3-4일",
                "budget": "상"
            },
            {
                "place": "🏢 오사카 (비즈니스 네트워킹)",
                "description": "역사적 의미의 오사카성과 현대 도시",
                "attractions": ["오사카성", "비즈니스 디스트릭트", "기술 박물관", "도시 관광"],
                "duration": "2-3일",
                "budget": "중상"
            },
            {
                "place": "🎯 쿄토 (역사 속의 전략)",
                "description": "역사적인 정치/군사 유적지 탐방",
                "attractions": ["황궁", "도요토미 유산", "닌자 박물관", "사무라이 문화"],
                "duration": "2-3일",
                "budget": "중상"
            }
        ]
    },
    "ESTJ": {
        "name": "신뢰할 수 있는 관리자",
        "destinations": [
            {
                "place": "🗻 도쿄-오사카 황금코스",
                "description": "효율적으로 계획된 일본의 주요 관광지",
                "attractions": ["동경역", "오사카성", "교토 사찰", "엔닌자키"],
                "duration": "5-7일",
                "budget": "중상"
            },
            {
                "place": "🚄 신칸센 투어 (기차 여행)",
                "description": "일본의 체계적이고 안정적인 교통망 이용",
                "attractions": ["신칸센 경험", "각 도시 주요 관광지", "전통 관광", "료칸 숙박"],
                "duration": "4-5일",
                "budget": "중상"
            },
            {
                "place": "🎌 나라-오사카 역사 투어",
                "description": "일본 역사의 중요 유적지 체계적 탐방",
                "attractions": ["나라 대불", "도다이지", "오사카성", "역사박물관"],
                "duration": "2-3일",
                "budget": "중하"
            }
        ]
    },
    "ESFP": {
        "name": "생기 넘치는 연예인",
        "destinations": [
            {
                "place": "🎉 도쿄 (재미와 엔터테인먼트)",
                "description": "신나는 도시의 모든 재미를 즐기기",
                "attractions": ["가라오케", "클럽", "테마파크", "레이저 태그"],
                "duration": "3-4일",
                "budget": "상"
            },
            {
                "place": "🎪 오사카 (축제와 파티)",
                "description": "활기찬 야시장과 24시간 도시 활동",
                "attractions": ["도톤보리 나이트라이프", "축제", "클럽", "영화관"],
                "duration": "2-3일",
                "budget": "상"
            },
            {
                "place": "🏖️ 오키나와 (휴양지)",
                "description": "해변에서의 물놀이와 워터스포츠",
                "attractions": ["해변", "스노쿨링", "워터파크", "해변 바"],
                "duration": "3-4일",
                "budget": "중상"
            }
        ]
    },
    "ESFJ": {
        "name": "따뜻한 친구",
        "destinations": [
            {
                "place": "🌸 교토 (문화 공유)",
                "description": "사람들과 함께하는 전통 문화 체험",
                "attractions": ["게이샤 관광", "마츠리 축제", "온천마을", "전통 음식"],
                "duration": "3-4일",
                "budget": "중상"
            },
            {
                "place": "👥 오사카 (사람과의 만남)",
                "description": "따뜻한 현지인들과의 상호작용",
                "attractions": ["로컬 식당", "야시장", "축제", "커뮤니티 활동"],
                "duration": "2-3일",
                "budget": "중상"
            },
            {
                "place": "🎌 히로시마 (의미 있는 여행)",
                "description": "역사적 의미 있는 장소와 평화의 메시지",
                "attractions": ["평화기념공원", "히로시마성", "국제성", "추도섬"],
                "duration": "1-2일",
                "budget": "중하"
            }
        ]
    },
    "ISFP": {
        "name": "예민한 모험가",
        "destinations": [
            {
                "place": "🎨 가나자와 (예술 도시)",
                "description": "아름다운 정원과 예술 문화",
                "attractions": ["21세기미술관", "켄로쿠엔 정원", "게이샤 구역", "식사"],
                "duration": "2-3일",
                "budget": "중하"
            },
            {
                "place": "🌲 아라시야마 (자연 속 예술)",
                "description": "아름다운 자연경관과 예술 공간",
                "attractions":
