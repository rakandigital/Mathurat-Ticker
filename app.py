import streamlit as st
import pandas as pd
import requests
import datetime
import io
from streamlit_javascript import st_javascript

# ==========================================
# 1. CONFIG & CSS (Mobile-First UI)
# ==========================================
st.set_page_config(
    page_title="Mathurat Ticker",
    page_icon="📿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    
    .main {
        padding-top: 65px !important;
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
        padding: 10px 0;
    }
    
    @media (prefers-color-scheme: dark) {
        div[data-testid="stVerticalBlock"] > div:has(div.nav-container) {
            background-color: #0e1117;
            border-bottom: 1px solid #333;
        }
    }

    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 34px;
        text-align: center;
        direction: rtl;
        line-height: 2.5;
        margin-bottom: 20px;
        padding: 10px;
    }
    
    .section-title {
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
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
        background-color: #f8f9fa;
        color: #333;
        text-align: center;
        padding: 15px;
        font-size: 14px;
        border-top: 1px solid #ddd;
        z-index: 998;
    }
    @media (prefers-color-scheme: dark) {
        .footer { background-color: #161b22; color: #ccc; border-top: 1px solid #333; }
    }

    /* Floating Gundal Button Placement */
    div[data-testid="stVerticalBlock"] > div:last-child div.stButton > button {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 75px;
        height: 75px;
        border-radius: 50%;
        background-color: #2e7d32;
        color: white;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        border: none;
        z-index: 1000;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LAYER (List of Dicts = Safe CSV)
# ==========================================
def load_data():
    # This matches your CSV structure exactly
    return [
        {"id": 1, "order": 1, "title": "Al-Fatihah", "type": "quran", "surah": 1, "ayah": 1, "arabic": "", "transliteration": "Bismillah...", "translation_ms": "Dengan nama Allah Yang Maha Pemurah lagi Maha Mengasihani.", "translation_en": "In the name of Allah...", "repeat": 1, "session": "both", "set": "both"},
        {"id": 2, "order": 2, "title": "Al-Fatihah", "type": "quran", "surah": 1, "ayah": 2, "arabic": "", "transliteration": "Alhamdulillah...", "translation_ms": "Segala puji bagi Allah, Tuhan semesta alam.", "translation_en": "[All] praise is [due] to Allah...", "repeat": 1, "session": "both", "set": "both"},
        {"id": 3, "order": 3, "title": "Ayatul Kursi", "type": "quran", "surah": 2, "ayah": 255, "arabic": "", "transliteration": "Allahu la ilaha...", "translation_ms": "Allah, tiada Tuhan melainkan Dia...", "translation_en": "Allah - there is no deity except Him...", "repeat": 1, "session": "both", "set": "both"},
        {"id": 4, "order": 4, "title": "Istighfar", "type": "dua", "surah": "", "ayah": "", "arabic": "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ", "transliteration": "Astaghfirullah...", "translation_ms": "Aku memohon ampun kepada Allah...", "translation_en": "I seek forgiveness from Allah...", "repeat": 3, "session": "both", "set": "both"},
        {"id": 5, "order": 5, "title": "Doa Pagi", "type": "dua", "surah": "", "ayah": "", "arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ", "transliteration": "Asbahna...", "translation_ms": "Kami berpagi hari dan berpagi harilah kerajaan bagi Allah.", "translation_en": "We have reached the morning...", "repeat": 1, "session": "pagi", "set": "both"},
        {"id": 6, "order": 6, "title": "Doa Petang", "type": "dua", "surah": "", "ayah": "", "arabic": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ", "transliteration": "Amsaina...", "translation_ms": "Kami berpetang hari dan berpetang harilah kerajaan bagi Allah.", "translation_en": "We have reached the evening...", "repeat": 1, "session": "petang", "set": "both"}
    ]

@st.cache_data
def fetch_quran_text(surah, ayah):
    url = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/editions/quran-uthmani"
    try:
        r = requests.get(url, timeout=5)
        return r.json()['data'][0]['text'] if r.status_code == 200 else "Error fetching API."
    except: return "Connection Error."

# ==========================================
# 3. STATE & TIME
# ==========================================
device_hour = st_javascript("new Date().getHours()")

if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'tally' not in st.session_state: st.session_state.tally = 0
if 'df_active' not in st.session_state: st.session_state.df_active = []
if 'start_time' not in st.session_state: st.session_state.start_time = None

def start_reading(mathurat_set):
    st.session_state.start_time = datetime.datetime.now()
    # Detect session from device time
    h = device_hour if device_hour is not None else 8
    sess = 'pagi' if 5 <= h < 15 else 'petang'
    
    raw_data = load_data()
    # Filter content
    filtered = [
        row for row in raw_data 
        if (row['session'] == 'both' or row['session'] == sess) and 
           (row['set'] == 'both' or row['set'] == mathurat_set)
    ]
    st.session_state.df_active = sorted(filtered, key=lambda x: x['order'])
    st.session_state.current_idx = 0
    st.session_state.tally = 0
    st.session_state.page = 'reading'

def handle_gundal(rep):
    st.session_state.tally += 1
    if st.session_state.tally >= rep:
        if st.session_state.current_idx < len(st.session_state.df_active) - 1:
            st.session_state.current_idx += 1
            st.session_state.tally = 0
        else:
            st.session_state.page = 'end'

# ==========================================
# 4. UI SCREENS
# ==========================================

if st.session_state.page == 'landing':
    st.title("Mathurat Ticker")
    st.caption("Baca tanpa lupa.")
    mode = st.radio("Pilih Bacaan:", ["sughra", "kubra"])
    if st.button("START", type="primary", use_container_width=True):
        start_reading(mode)
        st.rerun()

elif st.session_state.page == 'reading':
    # Navigation Header
    st.markdown('<div class="nav-container"></div>', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        if st.button("PREV", use_container_width=True):
            st.session_state.current_idx = max(0, st.session_state.current_idx - 1)
            st.session_state.tally = 0
            st.rerun()
    with n2:
        if st.button("HOME", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
    with n3:
        if st.button("NEXT", use_container_width=True):
            if st.session_state.current_idx < len(st.session_state.df_active) - 1:
                st.session_state.current_idx += 1
                st.session_state.tally = 0
            else: st.session_state.page = 'end'
            st.rerun()

    # Content Area
    item = st.session_state.df_active[st.session_state.current_idx]
    st.markdown(f'<div class="section-title">{item["title"]}</div>', unsafe_allow_html=True)
    
    # Requirement: Quran from API, Dua from internal data
    if item['type'] == 'quran':
        with st.spinner("Loading..."):
            arabic = fetch_quran_text(item['surah'], item['ayah'])
    else:
        arabic = item['arabic']
        
    st.markdown(f'<div class="arabic-text">{arabic}</div>', unsafe_allow_html=True)
    
    if item['transliteration']:
        st.caption(item['transliteration'])
        
    with st.expander("Terjemahan"):
        st.write(f"**MS:** {item['translation_ms']}")
        st.divider()
        st.write(f"**EN:** {item['translation_en']}")

    # Progress & FAB
    rep = int(item['repeat'])
    st.metric("Gundal", f"{st.session_state.tally} / {rep}")
    
    label = "DONE" if st.session_state.tally + 1 >= rep else str(st.session_state.tally + 1)
    if st.button(label, key="fab", on_click=handle_gundal, args=(rep,)):
        pass

elif st.session_state.page == 'end':
    st.balloons()
    dur = datetime.datetime.now() - st.session_state.start_time
    st.success(f"Alhamdulillah. Selesai dalam {dur.seconds // 60} minit {dur.seconds % 60} saat.")
    if st.button("Kembali"):
        st.session_state.page = 'landing'
        st.rerun()

# Fixed Footer
st.markdown("""
<div class="footer">
    Support Us | <a href="https://www.bizappay.my/qIKzmsvfiX" target="_blank">Sumbangan Ikhlas</a>
</div>
""", unsafe_allow_html=True)
