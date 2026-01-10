import streamlit as st
import pandas as pd
import requests
import datetime
import io
from streamlit_javascript import st_javascript

# ==========================================
# 1. CONFIG & CSS
# ==========================================
st.set_page_config(
    page_title="Mathurat Ticker",
    page_icon="📿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Mobile-First, Fixed Header/Footer, and Floating Button
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Lateef&display=swap');
    
    .main {
        padding-top: 60px !important;
        padding-bottom: 100px !important;
    }

    /* Fixed Header Navigation */
    div[data-testid="stVerticalBlock"] > div:has(div.nav-container) {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 999;
        background-color: #ffffff;
        border-bottom: 1px solid #ddd;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    @media (prefers-color-scheme: dark) {
        div[data-testid="stVerticalBlock"] > div:has(div.nav-container) {
            background-color: #0e1117;
            border-bottom: 1px solid #333;
        }
    }

    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 32px;
        text-align: center;
        direction: rtl;
        line-height: 2.2;
        margin-bottom: 20px;
    }
    
    .section-title {
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        color: #888;
        font-size: 14px;
        text-transform: uppercase;
    }

    /* Fixed Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ddd;
        z-index: 998;
    }
    @media (prefers-color-scheme: dark) {
        .footer { background-color: #161b22; color: #ccc; border-top: 1px solid #333; }
    }

    /* FAB CSS */
    div[data-testid="stVerticalBlock"] > div:last-child div.stButton > button {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background-color: #4CAF50;
        color: white;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        border: none;
        z-index: 1000;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LAYER
# ==========================================
def load_data():
    csv_data = """id,order,title,type,surah,ayah,arabic,transliteration,translation_ms,translation_en,repeat,session,set
1,1,Al-Fatihah,quran,1,1,,Bismillah...,Dengan nama Allah...,In the name of Allah...,1,both,both
2,2,Ayatul Kursi,quran,2,255,,Allahu la ilaha...,Allah tiada Tuhan...,Allah! There is no deity...,1,both,both
3,3,Selawat Nabi,dua,,,اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَآلِ مُحَمَّدٍ,,Ya Allah, limpahkan rahmat...,Oh Allah send blessings...,3,both,both
4,4,Doa Pagi,dua,,,أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ,,Kami berpagi hari...,We have entered morning...,3,pagi,both
5,5,Doa Petang,dua,,,أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ,,Kami berpetang hari...,We have entered evening...,3,petang,both
"""
    df = pd.read_csv(io.StringIO(csv_data))
    df.fillna('', inplace=True)
    return df

@st.cache_data
def fetch_quran_text(surah, ayah):
    url = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/editions/quran-uthmani"
    try:
        response = requests.get(url, timeout=5)
        return response.json()['data'][0]['text'] if response.status_code == 200 else "Error."
    except: return "Connection error."

# ==========================================
# 3. DEVICE TIME COMPONENT (JS)
# ==========================================
# This gets the current hour from the user's browser
device_hour = st_javascript("new Date().getHours()")

# ==========================================
# 4. STATE MANAGEMENT & LOGIC
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'tally_count' not in st.session_state: st.session_state.tally_count = 0

def start_reading(mathurat_set):
    # Capture timestamp based on server but we will use device_hour for session logic
    st.session_state.start_time = datetime.datetime.now()
    
    # Session Detection (Using device hour captured via JS)
    # Default to 8 (morning) if JS hasn't returned yet
    hour = device_hour if device_hour is not None else 8
    time_session = 'pagi' if 5 <= hour < 15 else 'petang'
    
    raw_df = load_data()
    # Filtering logic
    mask = ((raw_df['session'] == 'both') | (raw_df['session'] == time_session)) & \
           ((raw_df['set'] == 'both') | (raw_df['set'] == mathurat_set))
    
    st.session_state.df_active = raw_df[mask].sort_values('order').reset_index(drop=True)
    st.session_state.page = 'reading'

# Navigation functions
def go_next():
    if st.session_state.current_index < len(st.session_state.df_active) - 1:
        st.session_state.current_index += 1
        st.session_state.tally_count = 0
    else: st.session_state.page = 'end'

def handle_gundal(repeat):
    st.session_state.tally_count += 1
    if st.session_state.tally_count >= repeat: go_next()

# ==========================================
# 5. UI RENDERING
# ==========================================

if st.session_state.page == 'landing':
    st.title("Mathurat Ticker")
    st.caption("Tagline: Baca tanpa lupa.")
    mode = st.radio("Pilih Set:", ["sughra", "kubra"])
    if st.button("START", type="primary", use_container_width=True):
        start_reading(mode)
        st.rerun()

elif st.session_state.page == 'reading':
    # Fixed Header
    st.markdown('<div class="nav-container"></div>', unsafe_allow_html=True)
    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col1: 
        if st.button("⬅", use_container_width=True): 
            st.session_state.current_index = max(0, st.session_state.current_index - 1)
            st.session_state.tally_count = 0
            st.rerun()
    with h_col2: 
        if st.button("🏠", use_container_width=True): 
            st.session_state.page = 'landing'
            st.rerun()
    with h_col3: 
        if st.button("➡", use_container_width=True): 
            go_next()
            st.rerun()

    # Content
    item = st.session_state.df_active.iloc[st.session_state.current_index]
    st.markdown(f'<div class="section-title">{item["title"]}</div>', unsafe_allow_html=True)
    
    arabic = fetch_quran_text(item['surah'], item['ayah']) if item['type'] == 'quran' else item['arabic']
    st.markdown(f'<div class="arabic-text">{arabic}</div>', unsafe_allow_html=True)
    
    with st.expander("Terjemahan"):
        st.write(item['translation_ms'])

    # FAB / Gundal
    rep = int(item['repeat'])
    st.metric("Gundal", f"{st.session_state.tally_count} / {rep}")
    
    label = "✔" if st.session_state.tally_count + 1 >= rep else str(st.session_state.tally_count + 1)
    if st.button(label, key="fab", on_click=handle_gundal, args=(rep,)):
        pass

elif st.session_state.page == 'end':
    dur = datetime.datetime.now() - st.session_state.start_time
    st.success(f"Alhamdulillah. Selesai dalam {dur.seconds // 60}m {dur.seconds % 60}s.")
    if st.button("Home"): 
        st.session_state.page = 'landing'
        st.rerun()

st.markdown('<div class="footer">Support Us | <a href="https://www.bizappay.my/qIKzmsvfiX">Donate</a></div>', unsafe_allow_html=True)
