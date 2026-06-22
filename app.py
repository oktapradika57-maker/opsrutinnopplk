import streamlit as st
import pandas as pd

# Konfigurasi Halaman (Wajib di paling atas)
st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- CUSTOM CSS UNTUK TAMPILAN PROFESIONAL ---
# Mengubah tombol default Streamlit menjadi seperti "Card" / Kartu Menu
st.markdown("""
    <style>
    /* Mengatur ukuran dan gaya tombol menu */
    div.stButton > button {
        height: 70px;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease-in-out;
        color: #333;
    }
    /* Efek ketika kursor diarahkan ke tombol */
    div.stButton > button:hover {
        border-color: #0066cc;
        box-shadow: 0 4px 8px rgba(0,102,204,0.15);
        color: #0066cc;
    }
    /* Mengatur jarak deskripsi menu di bawah tombol */
    .menu-desc {
        font-size: 13px;
        color: #666;
        margin-top: -10px;
        margin-bottom: 25px;
        text-align: center;
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
menu_options = [
    "Halaman Depan", 
    "1. Monitoring Varcost", 
    "2. Monitoring Preventive Maintenance", 
    "3. Monitoring Project", 
    "4. Monitoring KPI", 
    "5. Monitoring Asset", 
    "6. Monitoring Operational", 
    "7. Monitoring PJB"
]

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
    st.title("🏠 Dashboard Corporate Portal")
    st.markdown("<p style='font-size: 16px; color: #555;'>Pilih menu di bawah ini untuk mengakses detail monitoring dan performa.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Membuat Layout Grid (3 Kolom)
    col1, col2, col3 = st.columns(3)

    # --- Kolom 1 ---
    with col1:
        if st.button("💰 1. Monitoring Varcost", use_container_width=True):
            navigate_to("1. Monitoring Varcost")
        st.markdown("<div class='menu-desc'>Report & Analisa Variable Cost</div>", unsafe_allow_html=True)

        if st.button("🎯 4. Monitoring KPI", use_container_width=True):
            navigate_to("4. Monitoring KPI")
        st.markdown("<div class='menu-desc'>Analisa & Perhitungan KPI Karyawan</div>", unsafe_allow_html=True)

    # --- Kolom 2 ---
    with col2:
        if st.button("🔧 2. Preventive Maintenance", use_container_width=True):
            navigate_to("2. Monitoring Preventive Maintenance")
        st.markdown("<div class='menu-desc'>Pencapaian PM & Kurva S</div>", unsafe_allow_html=True)

        if st.button("🏢 5. Monitoring Asset", use_container_width=True):
            navigate_to("5. Monitoring Asset")
        st.markdown("<div class='menu-desc'>Asset KUT, Kisel, Rental & Depresiasi</div>", unsafe_allow_html=True)

    # --- Kolom 3 ---
    with col3:
        if st.button("🚀 3. Monitoring Project", use_container_width=True):
            navigate_to("3. Monitoring Project")
        st.markdown("<div class='menu-desc'>Daftar Project & Timeline Progress</div>", unsafe_allow_html=True)

        if st.button("⚙️ 6. Monitoring Operational", use_container_width=True):
            navigate_to("6. Monitoring Operational")
        st.markdown("<div class='menu-desc'>Analisa BBM Mobil, Motor, & Genset</div>", unsafe_allow_html=True)

    # --- Area Bawah Tengah (Untuk Menu ke-7) ---
    st.write("") # Spasi
    col_empty1, col_center, col_empty2 = st.columns([1, 1, 1])
    with col_center:
        if st.button("📑 7. Monitoring PJB", use_container_width=True):
            navigate_to("7. Monitoring PJB")
        st.markdown("<div class='menu-desc'>Tracking Aging Berkas Pengajuan</div>", unsafe_allow_html=True)

# =========================================================
# ISI MASING-MASING HALAMAN
# =========================================================

elif page == "1. Monitoring Varcost":
    st.title("Monitoring Varcost")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"))
    st.markdown("---")
    
    # Ganti 'Varcost' dengan nama Sheet asli di Google Sheets Anda
    df_varcost = load_data("Varcost") 
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True)
    else:
        st.info("Data belum tersedia atau nama sheet tidak cocok.")

# ... (Menu 2 hingga 7 tetap menggunakan struktur yang sama seperti sebelumnya) ...
elif page == "7. Monitoring PJB":
    st.title("Monitoring PJB")
    st.button("⬅ Kembali ke Home", on_click=lambda: navigate_to("Halaman Depan"))
    st.markdown("---")
    st.write("Area Aging Berkas Pengajuan")
