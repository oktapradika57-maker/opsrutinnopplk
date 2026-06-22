import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Corporate Dashboard", layout="wide", page_icon="📊")

# --- 1. INISIALISASI SESSION STATE UNTUK NAVIGASI ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Halaman Depan"

# Fungsi untuk berpindah halaman ketika tombol ditekan
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# --- 2. FUNGSI UNTUK MENARIK DATA DARI GOOGLE SHEETS ---
@st.cache_data(ttl=600)
def load_data(sheet_name):
    sheet_id = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
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

st.sidebar.title("🧭 Navigasi")
# Radio button di sidebar yang tersinkronisasi dengan session_state
selected_page = st.sidebar.radio(
    "Pilih Halaman:",
    menu_options,
    index=menu_options.index(st.session_state.current_page)
)

# Jika user nge-klik dari sidebar, update session state dan muat ulang
if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()


# --- 4. KONTEN HALAMAN ---
page = st.session_state.current_page

if page == "Halaman Depan":
    st.title("🏠 Dashboard Corporate Portal")
    st.markdown("Selamat datang di pusat pemantauan performa dan operasional. Silakan pilih menu di bawah ini untuk masuk ke masing-masing dashboard.")
    st.divider()

    # Membuat Layout Grid (3 Kolom) untuk menu navigasi halaman depan
    col1, col2, col3 = st.columns(3)

    # --- Kolom 1 ---
    with col1:
        st.success("💰 **1. Monitoring Varcost**")
        st.caption("Report & Analisa Variable Cost")
        if st.button("Buka Dashboard Varcost ➡", use_container_width=True):
            navigate_to("1. Monitoring Varcost")
            
        st.write("") # Spasi
        st.write("")
        
        st.warning("🎯 **4. Monitoring KPI**")
        st.caption("Analisa & Perhitungan KPI")
        if st.button("Buka Dashboard KPI ➡", use_container_width=True):
            navigate_to("4. Monitoring KPI")

    # --- Kolom 2 ---
    with col2:
        st.info("🔧 **2. Preventive Maintenance**")
        st.caption("Pencapaian PM & Kurva S")
        if st.button("Buka Dashboard PM ➡", use_container_width=True):
            navigate_to("2. Monitoring Preventive Maintenance")
            
        st.write("")
        st.write("")
        
        st.error("🏢 **5. Monitoring Asset**")
        st.caption("Asset KUT, Kisel, Rental & Depresiasi")
        if st.button("Buka Dashboard Asset ➡", use_container_width=True):
            navigate_to("5. Monitoring Asset")

    # --- Kolom 3 ---
    with col3:
        st.info("🚀 **3. Monitoring Project**")
        st.caption("Daftar Project & Timeline")
        if st.button("Buka Dashboard Project ➡", use_container_width=True):
            navigate_to("3. Monitoring Project")
            
        st.write("")
        st.write("")
        
        st.success("⚙️ **6. Monitoring Operational**")
        st.caption("Analisa BBM Mobil, Motor, & Genset")
        if st.button("Buka Dashboard Operational ➡", use_container_width=True):
            navigate_to("6. Monitoring Operational")

    st.divider()
    
    # --- Kolom Tengah Bawah (Untuk menu ke-7) ---
    col_empty1, col_center, col_empty2 = st.columns([1, 1, 1])
    with col_center:
        st.warning("📑 **7. Monitoring PJB**")
        st.caption("Aging Berkas Pengajuan")
        if st.button("Buka Dashboard PJB ➡", use_container_width=True):
            navigate_to("7. Monitoring PJB")

# =========================================================
# ISI MASING-MASING HALAMAN (Sama seperti sebelumnya)
# =========================================================

elif page == "1. Monitoring Varcost":
    st.title("Monitoring Varcost")
    st.button("⬅ Kembali ke Halaman Depan", on_click=lambda: navigate_to("Halaman Depan"))
    st.divider()
    
    df_varcost = load_data("Varcost") # Ganti dengan nama Sheet asli
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True)

elif page == "2. Monitoring Preventive Maintenance":
    st.title("Monitoring Preventive Maintenance")
    st.button("⬅ Kembali ke Halaman Depan", on_click=lambda: navigate_to("Halaman Depan"))
    st.divider()
    # Logika isi PM ...

elif page == "3. Monitoring Project":
    st.title("Monitoring Project")
    st.button("⬅ Kembali ke Halaman Depan", on_click=lambda: navigate_to("Halaman Depan"))
    st.divider()
    # Logika isi Project ...

elif page == "4. Monitoring KPI":
    st.title("Monitoring KPI")
    st.button("⬅ Kembali ke Halaman Depan", on_click=lambda: navigate_to("Halaman Depan"))
    st.divider()
    # Logika isi KPI ...

elif page == "5. Monitoring Asset":
    st.title("Monitoring Asset")
    st.button("⬅ Kembali ke Halaman Depan", on_click=lambda: navigate_to("Halaman Depan"))
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["Asset KUT", "Asset Kisel", "Asset Rental"])
    with tab1:
        st.write("Data Asset KUT")
    with tab2:
        st.write("Data Asset Kisel")
    with tab3:
        st.write("Data Asset Rental")

elif page == "6. Monitoring Operational":
    st.title("Monitoring Operational")
    st.button("⬅ Kembali ke Halaman Depan", on_click=lambda: navigate_to("Halaman Depan"))
    st.divider()
    # Logika isi Operasional ...

elif page == "7. Monitoring PJB":
    st.title("Monitoring PJB")
    st.button("⬅ Kembali ke Halaman Depan", on_click=lambda: navigate_to("Halaman Depan"))
    st.divider()
    # Logika isi PJB ...
