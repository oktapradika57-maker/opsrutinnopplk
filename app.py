import streamlit as st

# 1. Konfigurasi Halaman (Mengaktifkan layout melebar/wide)
st.set_page_config(
    page_title="Corporate Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Judul Dasbor (Opsional)
st.title("📊 Enterprise Analytics Dashboard")
st.markdown("---")

# 3. Membuat Susunan Grid Menu yang Presisi (6 Kolom Sesuai Jumlah Menu)
# Menggunakan st.columns agar tombol berjejer rapi ke samping secara otomatis
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Menu 1: VARCOST
with col1:
    if st.button("💰\n\nVARCOST", use_container_width=True):
        st.session_state.active_menu = "VARCOST"

# Menu 2: KPI
with col2:
    if st.button("📈\n\nKPI", use_container_width=True):
        st.session_state.active_menu = "KPI"

# Menu 3: MAINTENANCE
with col3:
    if st.button("🛠️\n\nMAINTENANCE", use_container_width=True):
        st.session_state.active_menu = "MAINTENANCE"

# Menu 4: ASSET
with col4:
    if st.button("🏢\n\nASSET", use_container_width=True):
        st.session_state.active_menu = "ASSET"

# Menu 5: PROJECT
with col5:
    if st.button("🚀\n\nPROJECT", use_container_width=True):
        st.session_state.active_menu = "PROJECT"

# Menu 6: OPERATIONAL (Ejaan sudah diperbaiki)
with col6:
    if st.button("⚙️\n\nOPERATIONAL", use_container_width=True):
        st.session_state.active_menu = "OPERATIONAL"

st.markdown("---")

# 4. Logika Konten (Menampilkan halaman sesuai menu yang diklik)
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST" # Menu default saat pertama buka

st.subheader(f"Halaman: {st.session_state.active_menu}")

# Contoh visualisasi konten berdasarkan menu aktif
if st.session_state.active_menu == "VARCOST":
    st.info("Menampilkan metrik Variable Cost (Biaya Variabel)...")
    # Anda bisa memasukkan grafik/tabel data Anda di sini
    
elif st.session_state.active_menu == "KPI":
    st.success("Menampilkan indikator Key Performance Indicator...")
    
elif st.session_state.active_menu == "MAINTENANCE":
    st.warning("Menampilkan jadwal dan status Pemeliharaan Aset...")
