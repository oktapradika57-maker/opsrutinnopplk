import streamlit as st
import pandas as pd

# Konfigurasi Halaman (Wajib di paling atas)
st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- CUSTOM CSS UNTUK TAMPILAN 3D & BACKGROUND ---
st.markdown("""
    <style>
    /* 1. MENGATUR BACKGROUND HALAMAN */
    .stApp {
        /* Ganti URL di bawah ini dengan link gambar/logo Kinarya Utama Teknik Anda */
        background-image: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi9rl3YaSTLJw3M-PoWjndDGvx6DG3OO9yJxBOh1a8ZUyPG_6yk0TPnOvoEe7mt6yiD858V8dNcPmIay6e6LBVDf2EH0U9viZXZSuH6f-DM8dl3Q-NTHY3L0WTd3plcbKUOlgefUU6JfLC-rcIRyeDvM3S7gXcCWZkjrMNVSNbH3uLDKoIGKyVECGRGXSA/w680/koperasi-jasa-konstruksi-tower-event-organizer-network-monitoring-telekomunikasi-kisel-group-logo-kut.png");
        background-color: #f0f2f6; /* Warna dasar jika gambar tidak dimuat */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Membuat efek kaca (Glassmorphism) pada kontainer utama agar teks tetap terbaca di atas background */
    .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(4px);
        margin-top: 2rem;
    }

    /* 2. EFEK TOMBOL 3D (Neumorphism) */
    div.stButton > button {
        height: 80px;
        font-size: 17px !important;
        font-weight: 700 !important;
        border-radius: 15px;
        border: none;
        /* Warna gradasi dasar */
        background: linear-gradient(145deg, #ffffff, #e6e6e6);
        /* Efek timbul (shadow luar) */
        box-shadow: 6px 6px 12px #d1d1d1, -6px -6px 12px #ffffff;
        color: #333333;
        transition: all 0.2s ease-in-out;
    }
    
    /* Efek saat kursor diarahkan (Hover) */
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 8px 8px 16px #c4c4c4, -8px -8px 16px #ffffff;
        color: #0055ff;
    }
    
    /* Efek saat tombol diklik (Active/Ditekan ke dalam) */
    div.stButton > button:active {
        transform: translateY(2px);
        box-shadow: inset 6px 6px 12px #d1d1d1, inset -6px -6px 12px #ffffff;
    }

    /* Mengatur jarak deskripsi menu */
    .menu-desc {
        font-size: 14px;
        color: #555;
        margin-top: -5px;
        margin-bottom: 25px;
        text-align: center;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. INISIALISASI SESSION STATE UNTUK NAVIGASI ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Halaman Depan"

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# --- 2. FUNGSI UNTUK MENARIK DATA ---
@st.cache_data(ttl=600)
def load_data(sheet_name):
    sheet_id = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        return pd.read_csv(url)
    except Exception:
        return pd.DataFrame()

# --- 3. PENGATURAN SIDEBAR ---
# Nomor sudah dihilangkan dari daftar menu
menu_options = [
    "Halaman Depan", 
    "Monitoring Varcost", 
    "Monitoring Preventive Maintenance", 
    "Monitoring Project", 
    "Monitoring KPI", 
    "Monitoring Asset", 
    "Monitoring Operational", 
    "Monitoring PJB"
]

# Menampilkan Logo di Sidebar (Ganti URL dengan link logo asli Anda)
st.sidebar.image("https://via.placeholder.com/300x100.png?text=Logo+Kinarya+Utama+Teknik", use_container_width=True)
st.sidebar.title("🧭 Navigasi Utama")

selected_page = st.sidebar.radio(
    "Pilih Halaman:",
    menu_options,
    index=menu_options.index(st.session_state.current_page)
)

if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()

# --- 4. KONTEN HALAMAN ---
page = st.session_state.current_page

if page == "Halaman Depan":
    st.title("🏠 Dashboard Kinarya Utama Teknik")
    st.markdown("<p style='font-size: 16px; color: #555;'>Pilih menu di bawah ini untuk mengakses detail monitoring dan performa.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Membuat Layout Grid (3 Kolom)
    col1, col2, col3 = st.columns(3)

    # --- Kolom 1 ---
    with col1:
        if st.button("💰 Monitoring Varcost", use_container_width=True):
            navigate_to("Monitoring Varcost")
        st.markdown("<div class='menu-desc'>Report & Analisa Variable Cost</div>", unsafe_allow_html=True)

        if st.button("🎯 Monitoring KPI", use_container_width=True):
            navigate_to("Monitoring KPI")
        st.markdown("<div class='menu-desc'>Analisa & Perhitungan KPI</div>", unsafe_allow_html=True)

    # --- Kolom 2 ---
    with col2:
        if st.button("🔧 Preventive Maintenance", use_container_width=True):
            navigate_to("Monitoring Preventive Maintenance")
        st.markdown("<div class='menu-desc'>Pencapaian PM & Kurva S</div>", unsafe_allow_html=True)

        if st.button("🏢 Monitoring Asset", use_container_width=True):
            navigate_to("Monitoring Asset")
        st.markdown("<div class='menu-desc'>Asset KUT, Kisel, Rental & Depresiasi</div>", unsafe_allow_html=True)

    # --- Kolom 3 ---
    with col3:
        if st.button("🚀 Monitoring Project", use_container_width=True):
            navigate_to("Monitoring Project")
        st.markdown("<div class='menu-desc'>Daftar Project & Timeline Progress</div>", unsafe_allow_html=True)

        if st.button("⚙️ Monitoring Operational", use_container_width=True):
            navigate_to("Monitoring Operational")
        st.markdown("<div class='menu-desc'>Analisa BBM Mobil, Motor, & Genset</div>", unsafe_allow_html=True)

    # --- Area Bawah Tengah (Untuk Menu PJB) ---
    st.write("") # Spasi
    col_empty1, col_center, col_empty2 = st.columns([1, 1, 1])
    with col_center:
        if st.button("📑 Monitoring PJB", use_container_width=True):
            navigate_to("Monitoring PJB")
        st.markdown("<div class='menu-desc'>Tracking Aging Berkas Pengajuan</div>", unsafe_allow_html=True)

# =========================================================
# ISI MASING-MASING HALAMAN (Semua tombol kembali sudah diperbaiki)
# =========================================================

elif page == "Monitoring Varcost":
    st.title("Monitoring Varcost")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"), key="back_varcost")
    st.markdown("---")
    
    df_varcost = load_data("Varcost") 
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True)
    else:
        st.info("Data belum tersedia. Pastikan nama sheet di GSheets sesuai.")

elif page == "Monitoring Preventive Maintenance":
    st.title("Monitoring Preventive Maintenance")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"), key="back_pm")
    st.markdown("---")
    st.write("Area untuk menampilkan Analisa pencapaian dan Kurva S.")

elif page == "Monitoring Project":
    st.title("Monitoring Project")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"), key="back_proj")
    st.markdown("---")
    st.write("Area untuk menampilkan bermacam project dan timeline.")

elif page == "Monitoring KPI":
    st.title("Monitoring KPI")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"), key="back_kpi")
    st.markdown("---")
    st.write("Area untuk Analisa KPI dan perhitungan KPI.")

elif page == "Monitoring Asset":
    st.title("Monitoring Asset")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"), key="back_asset")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Asset KUT", "Asset Kisel", "Asset Rental"])
    with tab1:
        st.write("Data Asset KUT dan nilai sewa/depresiasi")
    with tab2:
        st.write("Data Asset Kisel dan nilai sewa/depresiasi")
    with tab3:
        st.write("Data Asset Rental dan nilai sewa/depresiasi")

elif page == "Monitoring Operational":
    st.title("Monitoring Operational")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"), key="back_ops")
    st.markdown("---")
    st.write("Area Analisa Operasional: BBM Mobil, Motor, dan Genset.")

elif page == "Monitoring PJB":
    st.title("Monitoring PJB")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"), key="back_pjb")
    st.markdown("---")
    st.write("Area Tracking Aging dari berkas-berkas pengajuan.")
