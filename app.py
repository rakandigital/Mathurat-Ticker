import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Mathurat Ticker",
    page_icon="📿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =================================================
# CSS (MOBILE FIRST)
# =================================================
st.markdown("""
<style>
/* Reset */
html, body {
  margin: 0;
  padding: 0;
}

st.components.v1.html("""
<div class="fixed-header">
  <div class="nav">
    <button onclick="window.parent.postMessage('prev_clicked','*')">◀ Prev</button>
    <button onclick="window.parent.postMessage('home_clicked','*')">🏠 Home</button>
    <button onclick="window.parent.postMessage('next_clicked','*')">Next ▶</button>
  </div>
</div>
""", height=0)

st.components.v1.html("""
<button id="gundal-btn">📿</button>
<script>
document.getElementById("gundal-btn").onclick = function() {
  window.parent.postMessage("gundal_clicked","*");
};
</script>
""", height=0)

/* ===== Fixed Header ===== */
.fixed-header {
  position: fixed;
  top: 0;
  width: 100%;
  height: 56px;
  background: #ffffff;
  z-index: 9999;
  border-bottom: 1px solid #eaeaea;
}

.fixed-header .nav {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  padding: 8px 10px;
}

.fixed-header button {
  background: #f7f9f8;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 8px 6px;
  font-size: 13px;
}

/* ===== Page Body ===== */
.page-body {
  margin-top: 64px;
  padding: 0 14px 100px 14px;
}

/* ===== Arabic Text ===== */
.arabic {
  font-size: 28px;
  line-height: 2.1;
  text-align: center;
  margin: 24px 0;
}

/* ===== Translation ===== */
.translation {
  font-size: 14px;
  color: #555;
  text-align: center;
  margin-top: 12px;
}

/* ===== Floating Gundal ===== */
#gundal-btn {
  position: fixed;
  bottom: 84px;
  right: 18px;
  width: 60px;
  height: 60px;
  background: #4f7f6f;
  color: white;
  font-size: 26px;
  border-radius: 50%;
  border: none;
  box-shadow: 0 8px 20px rgba(0,0,0,0.18);
  z-index: 9999;
}

/* ===== Footer ===== */
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  background: #f7f9f8;
  border-top: 1px solid #eaeaea;
  text-align: center;
  padding: 10px;
  font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =================================================
# CONSTANTS
# =================================================
QURAN_API = "https://api.alquran.cloud/v1/ayah"
DONATION_LINK = "https://www.bizappay.my/qIKzmsvfiX"

# =================================================
# SESSION STATE INIT
# =================================================
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

# =================================================
# HELPERS
# =================================================
def detect_session():
    return "pagi" if datetime.now().hour < 12 else "petang"

@st.cache_data(show_spinner=False)
def load_csv():
    return pd.read_csv("mathurat.csv")

@st.cache_data(show_spinner=False)
def fetch_quran_ayah(surah, ayah):
    try:
        r = requests.get(
            f"{QURAN_API}/{int(surah)}:{int(ayah)}/quran-uthmani",
            timeout=5
        )
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

# =================================================
# HEADER
# =================================================
st.title("Mathurat Ticker")
st.caption("Baca tanpa lupa.")

# =================================================
# HOME PAGE
# =================================================
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

# =================================================
# READING PAGE
# =================================================
elif st.session_state.page == "read":

    # Fixed Header Navigation
    st.markdown('<div class="nav-header">', unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns(3)

    with nav1:
        if st.button("◀ Previous", use_container_width=True):
            if st.session_state.index > 0:
                st.session_state.index -= 1
                st.session_state.count = 0

    with nav2:
        if st.button("🏠 Home", use_container_width=True):
            go_home()

    with nav3:
        if st.button("Next ▶", use_container_width=True):
            next_item(force=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Content
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

    # Gundal Button
    pressed = st.button("📿", key="gundal", help="Tandakan bacaan", type="primary")
    if pressed:
        st.session_state.count += 1
        next_item()

# =================================================
# DONE PAGE
# =================================================
elif st.session_state.page == "done":

    duration = st.session_state.end_time - st.session_state.start_time
    mins, secs = divmod(int(duration.total_seconds()), 60)

    st.success("Alhamdulillah. Bacaan selesai.")
    st.write(f"Tempoh masa yang diambil ialah **{mins} minit {secs} saat**")

    if st.button("Kembali ke Home"):
        go_home()

# =================================================
# FOOTER
# =================================================
st.markdown(
    f"""
    <div class="footer">
        ❤️ <a href="{DONATION_LINK}" target="_blank">Support Us</a>
    </div>
    """,
    unsafe_allow_html=True
)