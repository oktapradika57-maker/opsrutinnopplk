import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- CSS ---
st.markdown("""
    <style>
    div.stButton > button {
        height: 90px !important;
        width: 100% !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border-radius: 20px !important;
        border: none !important;
        color: white !important;
        transition: all 0.4s ease !important;
    }
    div.stButton:nth-child(1) > button { background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%) !important; }
    div.stButton:nth-child(2) > button { background: linear-gradient(135deg, #A18CD1 0%, #FBC2EB 100%) !important; }
    div.stButton:nth-child(3) > button { background: linear-gradient(135deg, #84FAB0 0%, #8FD3F4 100%) !important; }
    div.stButton:nth-child(4) > button { background: linear-gradient(135deg, #FA709A 0%, #FEE140 100%) !important; }
    div.stButton:nth-child(5) > button { background: linear-gradient(135deg, #FFD3A5 0%, #FD6585 100%) !important; }
    div.stButton:nth-child(6) > button { background: linear-gradient(135deg, #5EE7DF 0%, #B490CA 100%) !important; }
    div.stButton:nth-child(7) > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }
    
    div.stButton > button:hover { transform: scale(1.03); filter: brightness(1.1); }
    .menu-desc { font-size: 13px; color: #444; margin-top: 5px; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI ---
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

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
    
    # Menggunakan list agar mudah diatur tata letaknya
    menus = [
        ("💰 Varcost", "Monitoring Varcost", "Analisa Variable Cost"),
        ("🎯 KPI", "Monitoring KPI", "Perhitungan KPI"),
        ("🔧 Maintenance", "Monitoring Preventive Maintenance", "Pencapaian PM & Kurva S"),
        ("🏢 Asset", "Monitoring Asset", "Management Asset KUT"),
        ("🚀 Project", "Monitoring Project", "Timeline & Progress"),
        ("⚙️ Operational", "Monitoring Operational", "Analisa BBM & Genset"),
        ("📑 PJB", "Monitoring PJB", "Tracking Aging Berkas")
    ]
    
    # Membagi ke 3 kolom secara otomatis
    cols = st.columns(3)
    for i, (label, target, desc) in enumerate(menus):
        with cols[i % 3]:
            if st.button(label): navigate_to(target)
            st.markdown(f"<div class='menu-desc'>{desc}</div>", unsafe_allow_html=True)

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Home"): navigate_to("Halaman Depan")
    st.markdown("---")
    st.info(f"Halaman {st.session_state.current_page} sedang dimuat...")
