import streamlit as st
import pandas as pd

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Membuat grid container yang presisi */
    .menu-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        padding: 20px;
    }
    
    /* Tombol dengan ukuran tetap dan desain seragam */
    div.stButton > button {
        width: 100% !important;
        height: 180px !important;
        border-radius: 20px !important;
        border: 2px solid #ffffff !important;
        background-color: #262730 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
        /* Mengatur posisi teks di bawah gambar */
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-end !important;
        align-items: center !important;
        padding-bottom: 20px !important;
    }
    
    /* Memberikan efek visual gambar di dalam tombol */
    .btn-img {
        width: 80px;
        height: 80px;
        margin-bottom: 10px;
        object-fit: contain;
    }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("Dashboard Kinarya Utama Teknik")
    
    # URL gambar Anda
    img_url = "https://img.freepik.com/free-vector/team-goals-concept-illustration_114360-5290.jpg"
    
    menus = [
        ("Varcost", "Monitoring Varcost"), ("KPI", "Monitoring KPI"), 
        ("Maintenance", "Monitoring Preventive Maintenance"), ("Asset", "Monitoring Asset"),
        ("Project", "Monitoring Project"), ("Operational", "Monitoring Operational")
    ]
    
    # Membuat Grid
    st.markdown('<div class="menu-grid">', unsafe_allow_html=True)
    
    # Kita buat kolom manual untuk menampung button Streamlit
    cols = st.columns(3)
    for i, (label, target) in enumerate(menus):
        with cols[i % 3]:
            # Menampilkan gambar sebelum tombol agar presisi
            st.image(img_url, width=100)
            if st.button(label, key=label):
                navigate_to(target)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "Monitoring Asset":
    st.title("Monitoring Asset")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["Asset KUT", "Asset Rental"])
    with tab1: st.write("Data Asset KUT")
    with tab2: st.write("Data Asset Rental")
else:
    st.title(st.session_state.current_page)
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
