import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
from googleapiclient.discovery import build
from datetime import datetime
import re
from collections import Counter
from konlpy.tag import Okt
import warnings

warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="유튜브 댓글 분석기",
    page_icon="📊",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main { padding: 2rem; }
    .stTitle { color: #FF0000; }
    h1, h2, h3 { color: #1f77b4; }
    .metric-card { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("🎬 유튜브 댓글 분석기")

# ===================== 사이드바 설정 =====================
st.sidebar.header("⚙️ 설정")

api_key = st.sidebar.text_input(
    "YouTube API Key 입력",
    type="password",
    help="https://console.cloud.google.com 에서 API 키 발급"
)

youtube_url = st.sidebar.text_input(
    "YouTube 영상 링크 입력",
    placeholder="https://www.youtube.com/watch?v=..."
)

num_comments = st.sidebar.slider(
    "분석할 댓글 개수",
    min_value=10,
    max_value=1000,
    value=100,
    step=10
)

# ===================== 함수 정의 =====================

def extract_video_id(url):
    """유튜브 URL에서 비디오 ID 추출"""
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([^?]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_comments(api_key, video_id, max_comments):
    """유튜브 댓글 수집"""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        comments_data = []
        request = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100,
            order='relevance'
        )
        
        progress_bar = st.progress(0)
        
        while request and len(comments_data) < max_comments:
            response = request.execute()
            
            for item in response['items']:
                if len(comments_data) >= max_comments:
                    break
                
                comment = item['snippet']['topLevelComment']['snippet']
                comments_data.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt'],
                    'reply_count': item['snippet']['totalReplyCount']
                })
            
            progress = min(len(comments_data) / max_comments, 1.0)
            progress_bar.progress(progress)
            
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    pageToken=response['nextPageToken'],
                    textFormat='plainText',
                    maxResults=100,
                    order='relevance'
                )
            else:
                break
        
        progress_bar.empty()
        return pd.DataFrame(comments_data)
    
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        return None

def clean_text(text):
    """텍스트 전처리"""
    text = re.sub(r'[^\w\s가-힣]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_korean_nouns(text):
    """한글 명사 추출"""
    okt = Okt()
    try:
        nouns = okt.nouns(text)
        return [noun for noun in nouns if len(noun) > 1]
    except:
        return []

def get_video_info(api_key, video_id):
    """유튜브 영상 정보 조회"""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )
        response = request.execute()
        
        if response['items']:
            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'channel': video['snippet']['channelTitle'],
                'thumbnail': video['snippet']['thumbnails']['maxres']['url'],
                'views': int(video['statistics']['viewCount']),
                'likes': int(video['statistics'].get('likeCount', 0)),
                'comment_count': int(video['statistics'].get('commentCount', 0))
            }
    except:
        pass
    return None

def plot_comments_timeline(df):
    """시간대별 댓글 추이"""
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['date'] = df['published_at'].dt.date
    
    timeline = df.groupby('date').size().reset_index(name='count')
    
    fig = px.line(
        timeline,
        x='date',
        y='count',
        title='📈 시간대별 댓글 작성 추이',
        labels={'date': '날짜', 'count': '댓글 수'},
        markers=True
    )
    fig.update_traces(line=dict(color='#FF0000', width=2))
    return fig

def plot_likes_distribution(df):
    """댓글 반응도 분포"""
    fig = px.histogram(
        df,
        x='likes',
        nbins=50,
        title='👍 댓글 좋아요 분포',
        labels={'likes': '좋아요 수', 'count': '댓글 수'},
        color_discrete_sequence=['#FF0000']
    )
    return fig

def create_wordcloud(df):
    """한글 워드클라우드 생성"""
    # 텍스트 전처리
    texts = df['text'].apply(lambda x: clean_text(x)).tolist()
    
    # 명사 추출
    all_nouns = []
    for text in texts:
        nouns = extract_korean_nouns(text)
        all_nouns.extend(nouns)
    
    if not all_nouns:
        return None
    
    # 단어 빈도 계산
    noun_freq = Counter(all_nouns)
    
    # 워드클라우드 생성
    wc = WordCloud(
        font_path='/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        background_color='white',
        width=800,
        height=400,
        relative_scaling=0.5,
        min_font_size=10,
        collocations=False
    ).generate_from_frequencies(noun_freq)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    return fig

def plot_reply_count(df):
    """댓글 답글 수 분포"""
    df_top = df.nlargest(15, 'reply_count')
    
    fig = px.bar(
        df_top,
        x='reply_count',
        y='author',
        orientation='h',
        title='💬 가장 많은 답글을 받은 댓글 (상위 15개)',
        labels={'reply_count': '답글 수', 'author': '작성자'},
        color='reply_count',
        color_continuous_scale='Reds'
    )
    return fig

# ===================== 메인 로직 =====================

if not api_key:
    st.warning("⚠️ 사이드바에서 API 키를 입력하세요.")
    st.markdown("""
    ### API 키 발급 방법
    1. [Google Cloud Console](https://console.cloud.google.com) 접속
    2. 새 프로젝트 생성
    3. YouTube Data API v3 활성화
    4. 사용자 인증정보 > API 키 생성
    5. 키를 위 입력란에 붙여넣기
    """)

elif not youtube_url:
    st.info("💡 유튜브 영상 링크를 입력하세요.")

else:
    video_id = extract_video_id(youtube_url)
    
    if not video_id:
        st.error("❌ 유효한 유튜브 링크가 아닙니다.")
    else:
        # 영상 정보 조회
        with st.spinner("영상 정보 로드 중..."):
            video_info = get_video_info(api_key, video_id)
        
        if video_info:
            # 영상 정보 표시
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(video_info['thumbnail'], use_column_width=True)
            
            with col2:
                st.subheader(video_info['title'])
                st.markdown(f"**채널:** {video_info['channel']}")
                
                metric_cols = st.columns(3)
                with metric_cols[0]:
                    st.metric("조회수", f"{video_info['views']:,}")
                with metric_cols[1]:
                    st.metric("좋아요", f"{video_info['likes']:,}")
                with metric_cols[2]:
                    st.metric("댓글 수", f"{video_info['comment_count']:,}")
        
        st.divider()
        
        # 댓글 수집
        if st.button("🔍 댓글 분석 시작", use_container_width=True):
            with st.spinner(f"댓글 {num_comments}개 수집 중..."):
                df = get_youtube_comments(api_key, video_id, num_comments)
            
            if df is not None and len(df) > 0:
                st.success(f"✅ {len(df)}개의 댓글 수집 완료!")
                
                # 탭 생성
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📊 개요",
                    "📈 타임라인",
                    "👍 반응도",
                    "☁️ 워드클라우드",
                    "💬 인기 댓글"
                ])
                
                with tab1:
                    st.subheader("댓글 데이터 개요")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("총 댓글 수", len(df))
                    with col2:
                        st.metric("평균 좋아요", f"{df['likes'].mean():.1f}")
                    with col3:
                        st.metric("최대 좋아요", df['likes'].max())
                    with col4:
                        st.metric("평균 답글 수", f"{df['reply_count'].mean():.1f}")
                    
                    st.divider()
                    st.subheader("최근 댓글")
                    df_display = df[['author', 'text', 'likes', 'reply_count']].head(20).copy()
                    df_display['text'] = df_display['text'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
                    st.dataframe(df_display, use_container_width=True)
                
                with tab2:
                    st.plotly_chart(plot_comments_timeline(df), use_container_width=True)
                
                with tab3:
                    st.plotly_chart(plot_likes_distribution(df), use_container_width=True)
                    st.divider()
                    st.plotly_chart(plot_reply_count(df), use_container_width=True)
                
                with tab4:
                    st.subheader("댓글 워드클라우드")
                    wc_fig = create_wordcloud(df)
                    if wc_fig:
                        st.pyplot(wc_fig, use_container_width=True)
                    else:
                        st.warning("워드클라우드를 생성할 수 없습니다.")
                
                with tab5:
                    st.subheader("인기 있는 댓글 (좋아요 상위 20개)")
                    df_top = df.nlargest(20, 'likes')[['author', 'text', 'likes', 'reply_count']]
                    
                    for idx, row in df_top.iterrows():
                        with st.container():
                            col1, col2 = st.columns([1, 20])
                            with col2:
                                st.markdown(f"**{row['author']}**")
                                st.write(row['text'])
                                st.caption(f"👍 {row['likes']} | 💬 {row['reply_count']}")
                            st.divider()
            
            else:
                st.error("댓글을 수집할 수 없습니다. API 키와 영상 ID를 확인하세요.")
