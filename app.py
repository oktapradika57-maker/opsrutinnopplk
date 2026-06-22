import streamlit as st
import pandas as pd

st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- CSS PRESISI DENGAN GAMBAR ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 150px !important; /* Tinggi seragam */
        border-radius: 20px !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        transition: 0.3s !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        background-size: cover !important;
        background-position: center !important;
        text-shadow: 1px 1px 2px #000;
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("---")
    
    # Daftar menu dengan link gambar (bisa diganti URL gambar Anda sendiri)
    # Gunakan gambar ikon/background yang simpel agar teks tetap terbaca
    menus = [
        ("Varcost", "Monitoring Varcost", "https://img.freepik.com/free-vector/finance-concept-illustration_114360-3944.jpg"),
        ("KPI", "Monitoring KPI", "https://img.freepik.com/free-vector/target-marketing-concept-illustration_114360-3793.jpg"),
        ("Maintenance", "Monitoring Preventive Maintenance", "https://img.freepik.com/free-vector/mechanic-working-car-concept-illustration_114360-1490.jpg"),
        ("Asset", "Monitoring Asset", "https://img.freepik.com/free-vector/inventory-management-concept-illustration_114360-3843.jpg"),
        ("Project", "Monitoring Project", "https://img.freepik.com/free-vector/project-management-concept-illustration_114360-2374.jpg"),
        ("Operational", "Monitoring Operational", "https://img.freepik.com/free-vector/fuel-pump-concept-illustration_114360-3840.jpg")
    ]
    
    cols = st.columns(3)
    for i, (label, target, img_url) in enumerate(menus):
        # Mengatur background gambar per tombol melalui CSS injeksi
        st.markdown(f"""
            <style>
            div.stButton:nth-child({i+1}) > button {{
                background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{img_url}') !important;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        with cols[i % 3]:
            if st.button(label): navigate_to(target)
            st.write("") # Spacer

elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT")
    with tab2: st.write("Data Asset Rental")

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    st.write(f"Konten untuk {st.session_state.current_page} sedang disiapkan.")
