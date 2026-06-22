import streamlit as st

# 1. Konfigurasi Halaman (Mengaktifkan layout melebar/wide)
st.set_page_config(
    page_title="Corporate Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inisialisasi menu aktif di session state jika belum ada
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST"

# ==========================================
# 2. NAVIGASI ATAS (PRESISI & INSTAN)
# ==========================================
# Membuat 6 kolom yang sama rata ukurannya secara matematis
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Menu 1: VARCOST
with col1:
    if st.button("💰\n\nVARCOST", use_container_width=True, key="btn_varcost"):
        st.session_state.active_menu = "VARCOST"
        st.rerun() # Langsung muat ulang halaman secara instan

# Menu 2: KPI
with col2:
    if st.button("📈\n\nKPI", use_container_width=True, key="btn_kpi"):
        st.session_state.active_menu = "KPI"
        st.rerun()

# Menu 3: MAINTENANCE
with col3:
    if st.button("🛠️\n\nMAINTENANCE", use_container_width=True, key="btn_maint"):
        st.session_state.active_menu = "MAINTENANCE"
        st.rerun()

# Menu 4: ASSET
with col4:
    if st.button("🏢\n\nASSET", use_container_width=True, key="btn_asset"):
        st.session_state.active_menu = "ASSET"
        st.rerun()

# Menu 5: PROJECT
with col5:
    if st.button("🚀\n\nPROJECT", use_container_width=True, key="btn_project"):
        st.session_state.active_menu = "PROJECT"
        st.rerun()

# Menu 6: OPERATIONAL
with col6:
    if st.button("⚙️\n\nOPERATIONAL", use_container_width=True, key="btn_operational"):
        st.session_state.active_menu = "OPERATIONAL"
        st.rerun()

st.markdown("---")

# ==========================================
# 3. LOGIKA KONTEN HALAMAN (ROUTING)
# ==========================================
# Fungsi pembantu untuk memisahkan logika per halaman agar rapi

def halaman_varcost():
    st.subheader("💰 Halaman Variable Cost")
    st.info("Menampilkan metrik dan grafik Variable Cost (Biaya Variabel) Anda di sini.")
    # Saku/Tulis kode grafik atau tabel Pandas Anda di bawah ini

def halaman_kpi():
    st.subheader("📈 Halaman Key Performance Indicator")
    st.success("Menampilkan indikator pencapaian kinerja utama (KPI) perusahaan.")

def halaman_maintenance():
    st.subheader("🛠️ Halaman Maintenance")
    st.warning("Menampilkan jadwal dan status pemeliharaan mesin/perangkat.")

def halaman_asset():
    st.subheader("🏢 Halaman Asset")
    st.write("Daftar dan nilai manajemen aset perusahaan saat ini.")

def halaman_project():
    st.subheader("🚀 Halaman Project")
    st.write("Status perkembangan proyek berjalan saat ini.")

def halaman_operational():
    st.subheader("⚙️ Halaman Operational")
    st.write("Data harian terkait operasional lapangan.")


# Eksekusi fungsi halaman berdasarkan tombol menu yang sedang aktif
if st.session_state.active_menu == "VARCOST":
    halaman_varcost()
elif st.session_state.active_menu == "KPI":
    halaman_kpi()
elif st.session_state.active_menu == "MAINTENANCE":
    halaman_maintenance()
elif st.session_state.active_menu == "ASSET":
    halaman_asset()
elif st.session_state.active_menu == "PROJECT":
    halaman_project()
elif st.session_state.active_menu == "OPERATIONAL":
    halaman_operational()
