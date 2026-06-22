import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- CSS ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 120px !important;
        border-radius: 15px !important;
        border: none !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        transition: 0.3s !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    div.stButton > button:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
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
    
    menus = [
        ("💰\nVarcost", "Monitoring Varcost", "#667eea"),
        ("🎯\nKPI", "Monitoring KPI", "#ff9a9e"),
        ("🔧\nMaintenance", "Monitoring Preventive Maintenance", "#a18cd1"),
        ("🏢\nAsset", "Monitoring Asset", "#84fab0"),
        ("🚀\nProject", "Monitoring Project", "#fa709a"),
        ("⚙️\nOperational", "Monitoring Operational", "#ffd3a5"),
        ("📑\nPJB", "Monitoring PJB", "#5ee7df")
    ]
    
    for i, (label, target, color) in enumerate(menus):
        st.markdown(f"""<style>div.stButton:nth-child({i+1}) > button {{ background: {color} !important; }}</style>""", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (label, target, color) in enumerate(menus):
        with cols[i % 3]:
            if st.button(label): navigate_to(target)

elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali ke Home"): navigate_to("Halaman Depan")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental", "📊 Ringkasan"])
    with tab1: st.write("Data Asset KUT...")
    with tab2: st.write("Data Asset Rental...")
    with tab3: st.write("Analisa & Depresiasi...")

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Home"): navigate_to("Halaman Depan")
    st.markdown("---")
    # Baris yang tadi error sudah diperbaiki di bawah ini:
    st.write(f"Konten untuk {st.session_state.current_page} sedang diproses.")
