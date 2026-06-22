import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- CUSTOM CSS (ANIMASI & WARNA) ---
st.markdown("""
    <style>
    .block-container { animation: fadeIn 1s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    div.stButton > button {
        height: 90px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border-radius: 20px !important;
        border: none !important;
        color: white !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    div.stButton:nth-child(1) > button { background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%) !important; }
    div.stButton:nth-child(2) > button { background: linear-gradient(135deg, #A18CD1 0%, #FBC2EB 100%) !important; }
    div.stButton:nth-child(3) > button { background: linear-gradient(135deg, #84FAB0 0%, #8FD3F4 100%) !important; }
    div.stButton:nth-child(4) > button { background: linear-gradient(135deg, #FA709A 0%, #FEE140 100%) !important; }
    div.stButton:nth-child(5) > button { background: linear-gradient(135deg, #FFD3A5 0%, #FD6585 100%) !important; }
    div.stButton:nth-child(6) > button { background: linear-gradient(135deg, #5EE7DF 0%, #B490CA 100%) !important; }
    
    div.stButton > button:hover {
        transform: scale(1.05) rotate(1deg);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        filter: brightness(1.1);
    }
    .menu-desc { font-size: 13px; color: #444; margin-top: 10px; margin-bottom: 30px; text-align: center; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI NAVIGASI & DATA ---
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

@st.cache_data(ttl=600)
def load_data(sheet_name):
    sheet_id = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try: return pd.read_csv(url)
    except: return pd.DataFrame()

# --- INISIALISASI ---
if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

# --- SIDEBAR ---
st.sidebar.title("🧭 Navigasi Utama")
menu_options = ["Halaman Depan", "Monitoring Varcost", "Monitoring Preventive Maintenance", 
                "Monitoring Project", "Monitoring KPI", "Monitoring Asset", "Monitoring Operational", "Monitoring PJB"]
selected_page = st.sidebar.radio("Pilih Halaman:", menu_options, index=menu_options.index(st.session_state.current_page))
if selected_page != st.session_state.current_page: navigate_to(selected_page)

# --- KONTEN ---
if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 Monitoring Varcost"): navigate_to("Monitoring Varcost")
        st.markdown("<div class='menu-desc'>Analisa Variable Cost</div>", unsafe_allow_html=True)
        if st.button("🎯 Monitoring KPI"): navigate_to("Monitoring KPI")
        st.markdown("<div class='menu-desc'>Perhitungan KPI</div>", unsafe_allow_html=True)

    with col2:
        if st.button("🔧 Preventive Maintenance"): navigate_to("Monitoring Preventive Maintenance")
        st.markdown("<div class='menu-desc'>Pencapaian PM & Kurva S</div>", unsafe_allow_html=True)
        if st.button("🏢 Monitoring Asset"): navigate_to("Monitoring Asset")
        st.markdown("<div class='menu-desc'>Management Asset KUT</div>", unsafe_allow_html=True)

    with col3:
        if st.button("🚀 Monitoring Project"): navigate_to("Monitoring Project")
        st.markdown("<div class='menu-desc'>Timeline & Progress</div>", unsafe_allow_html=True)
        if st.button("⚙️ Monitoring Operational"): navigate_to("Monitoring Operational")
        st.markdown("<div class='menu-desc'>Analisa BBM & Genset</div>", unsafe_allow_html=True)
    
    if st.button("📑 Monitoring PJB"): navigate_to("Monitoring PJB")
    st.markdown("<div class='menu-desc'>Tracking Aging Berkas Pengajuan</div>", unsafe_allow_html=True)

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Home"): navigate_to("Halaman Depan")
    st.markdown("---")
    
    df = load_data(st.session_state.current_page.replace("Monitoring ", ""))
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Data sedang dimuat atau belum tersedia untuk halaman ini.")
