import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- CSS YANG DIOPTIMALKAN UNTUK PRESISI ---
st.markdown("""
    <style>
    /* Mengatur tinggi container tombol agar selalu sama */
    div.stButton > button {
        width: 100% !important;
        height: 120px !important; /* Tinggi tetap agar presisi */
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
        padding: 10px !important;
    }
    
    /* Warna gradasi dengan gaya modern */
    div.stButton:nth-child(1) > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }
    div.stButton:nth-child(2) > button { background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%) !important; }
    div.stButton:nth-child(3) > button { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%) !important; }
    div.stButton:nth-child(4) > button { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%) !important; }
    div.stButton:nth-child(5) > button { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important; }
    div.stButton:nth-child(6) > button { background: linear-gradient(135deg, #ffd3a5 0%, #fd6585 100%) !important; }
    div.stButton:nth-child(7) > button { background: linear-gradient(135deg, #5ee7df 0%, #b490ca 100%) !important; }

    /* Hover effect */
    div.stButton > button:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    
    /* Menyembunyikan teks deskripsi yang memecah layout */
    .menu-desc { display: none; }
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
    
    # List menu dengan label yang menyatukan Nama Menu dan Deskripsi singkat
    menus = [
        ("Varcost\n(Variable Cost)", "Monitoring Varcost"),
        ("KPI\n(Analisa & Perhitungan)", "Monitoring KPI"),
        ("Maintenance\n(Pencapaian & Kurva S)", "Monitoring Preventive Maintenance"),
        ("Asset\n(KUT, Kisel, Rental)", "Monitoring Asset"),
        ("Project\n(Timeline & Progress)", "Monitoring Project"),
        ("Operational\n(BBM & Genset)", "Monitoring Operational"),
        ("PJB\n(Aging Berkas)", "Monitoring PJB")
    ]
    
    # Loop untuk membuat grid 3 kolom yang presisi
    cols = st.columns(3)
    for i, (label, target) in enumerate(menus):
        with cols[i % 3]:
            if st.button(label): navigate_to(target)
            st.write("") # Memberi sedikit jarak antar baris

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Home"): navigate_to("Halaman Depan")
    st.markdown("---")
    st.write(f"Konten untuk {st.session_state.current_page} akan ditampilkan di sini.")
