import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Mathurat Ticker",
    page_icon="📿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# THEME & CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>
/* Floating Gundal Button */
.gundal-btn {
    position: fixed;
    bottom: 90px;
    right: 24px;
    z-index: 1000;
}

.gundal-btn button {
    background-color: #4f7f6f;
    color: white;
    border-radius: 50%;
    width: 64px;
    height: 64px;
    font-size: 22px;
    border: none;
}

/* Footer */
footer {
    visibility: hidden;
}

.footer-custom {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #f5f7f6;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CONSTANTS
# -------------------------------------------------
DONATION_LINK = "https://www.bizappay.my/qIKzmsvfiX"
QURAN_API = "https://api.alquran.cloud/v1/ayah"

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
defaults = {
    "page": "home",
    "mathurat_set": None,
    "session_time": None,
    "start_time": None,
    "end_time": None,
    "data": [],
    "index": 0,
    "count": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def detect_session():
    return "pagi" if datetime.now().hour < 12 else "petang"

@st.cache_data(show_spinner=False)
def load_csv():
    return pd.read_csv("mathurat.csv")

@st.cache_data(show_spinner=False)
def fetch_quran_ayah(surah, ayah):
    try:
        url = f"{QURAN_API}/{int(surah)}:{int(ayah)}/quran-uthmani"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()["data"]["text"]
    except Exception:
        pass
    return "— Ayat gagal dimuatkan —"

def load_session_data():
    df = load_csv()
    filtered = df[
        df["set"].str.contains(st.session_state.mathurat_set)
        & df["session"].str.contains(st.session_state.session_time)
    ].sort_values("order")
    st.session_state.data = filtered.to_dict("records")

def go_home():
    for k in defaults:
        st.session_state[k] = defaults[k]

def next_item(force=False):
    item = st.session_state.data[st.session_state.index]
    if force or st.session_state.count >= item["repeat"]:
        if st.session_state.index < len(st.session_state.data) - 1:
            st.session_state.index += 1
            st.session_state.count = 0
        else:
            st.session_state.end_time = datetime.now()
            st.session_state.page = "done"

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("Mathurat Ticker")
st.caption("Baca tanpa lupa.")

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
if st.session_state.page == "home":

    st.subheader("Pilih bacaan")
    col1, col2 = st.columns(2)

    if col1.button("Mathurat Sugra", use_container_width=True):
        st.session_state.mathurat_set = "sughra"

    if col2.button("Mathurat Kubra", use_container_width=True):
        st.session_state.mathurat_set = "kubra"

    if st.session_state.mathurat_set:
        st.session_state.session_time = detect_session()
        st.info(f"Sesi bacaan: {st.session_state.session_time.capitalize()}")

        if st.button("Start", type="primary", use_container_width=True):
            st.session_state.start_time = datetime.now()
            load_session_data()
            st.session_state.page = "read"

# -------------------------------------------------
# READING PAGE
# -------------------------------------------------
elif st.session_state.page == "read":

    item = st.session_state.data[st.session_state.index]

    st.subheader(item["title"])

    if item["type"] == "quran":
        arabic = fetch_quran_ayah(item["surah"], item["ayah"])
    else:
        arabic = item["arabic"]

    st.markdown(
        f"<div style='text-align:center; font-size:28px; line-height:2'>{arabic}</div>",
        unsafe_allow_html=True
    )

    with st.expander("Transliteration"):
        st.write(item.get("transliteration", ""))

    with st.expander("Terjemahan"):
        st.write(item.get("translation_ms", ""))
        st.write(item.get("translation_en", ""))

    st.caption(f"Bacaan: {st.session_state.count} / {item['repeat']}")

    # Gundal Floating Button
    st.markdown('<div class="gundal-btn">', unsafe_allow_html=True)
    if st.button("📿"):
        st.session_state.count += 1
        next_item()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns(3)
    if col1.button("Previous"):
        if st.session_state.index > 0:
            st.session_state.index -= 1
            st.session_state.count = 0

    if col2.button("Home"):
        go_home()

    if col3.button("Next"):
        next_item(force=True)

# -------------------------------------------------
# DONE PAGE
# -------------------------------------------------
elif st.session_state.page == "done":

    duration = st.session_state.end_time - st.session_state.start_time
    minutes, seconds = divmod(int(duration.total_seconds()), 60)

    st.success("Alhamdulillah. Bacaan selesai.")
    st.write(f"Tempoh masa yang diambil ialah **{minutes} minit {seconds} saat**")

    if st.button("Kembali ke Home"):
        go_home()

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    f"""
    <div class="footer-custom">
        ❤️ <a href="{DONATION_LINK}" target="_blank">Support Us</a>
    </div>
    """,
    unsafe_allow_html=True
)
