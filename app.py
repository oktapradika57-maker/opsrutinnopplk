import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Konfigurasi Halaman & Tema Gelap Ops Center
st.set_page_config(
    page_title="Telco Corporate Dashboard - Reg Kalimantan", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inisialisasi session state untuk navigasi halaman jika belum ada
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST"

# Tautan Spreadsheet Utama (Database Reg Kalimantan)
URL_SPREADSHEET = "https://google.com"

# Fungsi resmi menggunakan st.connection untuk membaca data dari Google Sheet publik
@st.cache_data(ttl=60)
def ambil_data_sheet(nama_sheet):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL_SPREADSHEET, worksheet=nama_sheet)
        return df
    except Exception as e:
        st.error(f"Gagal memuat sheet '{nama_sheet}': {e}")
        return pd.DataFrame()

# ==========================================
# 2. NAVIGASI ATAS (8 MENU PRESISI & INSTAN)
# ==========================================
# Membagi layar menjadi 8 kolom simetris sesuai dengan seluruh resource tab yang tersedia
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    if st.button("💰\n\nVARCOST", use_container_width=True, key="btn_varcost"):
        st.session_state.active_menu = "VARCOST"
        st.rerun()
with col2:
    if st.button("🛠️\n\nDATA PM", use_container_width=True, key="btn_pm"):
        st.session_state.active_menu = "DATA_PM"
        st.rerun()
with col3:
    if st.button("🚀\n\nDATA PROJECT", use_container_width=True, key="btn_project"):
        st.session_state.active_menu = "DATA_PROJECT"
        st.rerun()
with col4:
    if st.button("🏢\n\nDATA ASSET", use_container_width=True, key="btn_asset"):
        st.session_state.active_menu = "DATA_ASSET"
        st.rerun()
with col5:
    if st.button("📈\n\nDATA KPI", use_container_width=True, key="btn_kpi"):
        st.session_state.active_menu = "DATA_KPI"
        st.rerun()
with col6:
    if st.button("⚙️\n\nDATA OPERATIONAL", use_container_width=True, key="btn_operational"):
        st.session_state.active_menu = "DATA_OPERATIONAL"
        st.rerun()
with col7:
    if st.button("⏳\n\nDATA PJB AGING", use_container_width=True, key="btn_pjb"):
        st.session_state.active_menu = "DATA_PJB"
        st.rerun()
with col8:
    if st.button("📡\n\nMONITORING MBP", use_container_width=True, key="btn_mbp"):
        st.session_state.active_menu = "MONITORING_MBP"
        st.rerun()

st.markdown("---")

# ==========================================
# 3. KONTEN HALAMAN (RESOURCE LIVE GOOGLE SHEETS)
# ==========================================

# --- MENU 1: TAB VARCOST ---
def halaman_varcost():
    st.title("🌐 Telecom Variable Cost Analysis")
    st.caption("Memantau ringkasan biaya operasional dan data finansial regional dari tab 'VARCOST'.")
    st.write("")

    df_varcost = ambil_data_sheet("VARCOST")

    # Dropdown Analisa jika struktur kolom finansial tersedia di spreadsheet Anda
    st.subheader("📊 Corporate Financial Dropdown")
    opsi_analisa = st.selectbox(
        "Pilih Lini Analisis Finansial:",
        ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
    )

    if opsi_analisa == "Revenue Analysis (Pendapatan)":
        if not df_varcost.empty and 'Bulan' in df_varcost.columns and 'Revenue' in df_varcost.columns:
            st.line_chart(df_varcost.set_index('Bulan')[['Revenue']])
        else:
            st.info("💡 Grafik pendapatan otomatis terbentuk jika kolom 'Bulan' dan 'Revenue' tersedia di dalam sheet.")
            
    elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
        if not df_varcost.empty and 'Bulan' in df_varcost.columns and 'Net Income' in df_varcost.columns:
            st.bar_chart(df_varcost.set_index('Bulan')[['Net Income']])
        else:
            st.info("💡 Grafik laba bersih otomatis terbentuk jika kolom 'Bulan' dan 'Net Income' tersedia di dalam sheet.")

    st.write("")
    st.subheader("📋 Data Sheet Riil: VARCOST")
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True, hide_index=True)
    else:
        st.caption("Lembar kerja 'VARCOST' kosong atau gagal dibaca.")

# --- MENU 2: TAB DATA PM ---
def halaman_data_pm():
    st.title("🛠️ Preventive Maintenance Log (data PM)")
    st.caption("Memantau rekam aktivitas pemeliharaan infrastruktur secara berkala.")
    df_pm = ambil_data_sheet("data PM")
    if not df_pm.empty:
        st.dataframe(df_pm, use_container_width=True, hide_index=True)
    else:
        st.caption("Lembar kerja 'data PM' kosong atau tidak ditemukan.")

# --- MENU 3: TAB DATA PROJECT ---
def halaman_data_project():
    st.title("🚀 Network Rollout & Deployment Progress (data Project)")
    st.caption("Status pembangunan jaringan, site baru, dan integrasi sistem telekomunikasi.")
    df_project = ambil_data_sheet("data Project")
    if not df_project.empty:
        st.dataframe(df_project, use_container_width=True, hide_index=True)
    else:
        st.caption("Lembar kerja 'data Project' kosong atau tidak ditemukan.")

# --- MENU 4: TAB DATA ASSET (DENGAN SUB-MENU KUT & RENTAL) ---
def halaman_data_asset():
    st.title("🏢 Asset Management Inventory (data Asset)")
    st.caption("Manajemen aset perangkat core, transmisi, menara (tower), dan fasilitas penunjang.")
    st.write("")

    # 1. Ambil data asli dari Google Sheets tab 'data Asset'
    df_asset = ambil_data_sheet("data Asset")

    if not df_asset.empty:
        # 2. Membuat Sub-Menu Presisi Menggunakan st.radio (Berjejer Horizontal)
        sub_menu = st.radio(
            "Pilih Kategori Kategori Asset:",
            ["Semua Asset", "Asset KUT", "Asset Rental"],
            horizontal=True
        )
        st.write("")

        # 💡 SILAKAN SESUAIKAN: Ganti 'Jenis Asset' di bawah ini dengan nama kolom asli di Google Sheets Anda
        nama_kolom_pemisah = "Jenis Asset" 

        # Jalankan pengecekan apakah kolom pemisah tersebut ada di spreadsheet
        if nama_kolom_pemisah in df_asset.columns:
            
            if sub_menu == "Semua Asset":
                st.subheader("📋 Daftar Seluruh Asset")
                st.dataframe(df_asset, use_container_width=True, hide_index=True)
                
            elif sub_menu == "Asset KUT":
                st.subheader("📦 Daftar Asset KUT")
                # Memfilter baris data yang mengandung kata 'KUT' (tidak sensitif huruf besar/kecil)
                df_kut = df_asset[df_asset[nama_kolom_pemisah].astype(str).str.contains("KUT", case=False, na=False)]
                
                if not df_kut.empty:
                    st.dataframe(df_kut, use_container_width=True, hide_index=True)
                else:
                    st.info("Tidak ada baris data dengan kategori 'KUT' ditemukan pada kolom tersebut.")
                    
            elif sub_menu == "Asset Rental":
                st.subheader("🔑 Daftar Asset Rental")
                # Memfilter baris data yang mengandung kata 'Rental' (tidak sensitif huruf besar/kecil)
                df_rental = df_asset[df_asset[nama_kolom_pemisah].astype(str).str.contains("Rental", case=False, na=False)]
                
                if not df_rental.empty:
                    st.dataframe(df_rental, use_container_width=True, hide_index=True)
                else:
                    st.info("Tidak ada baris data dengan kategori 'Rental' ditemukan pada kolom tersebut.")
        
        else:
            # Jika nama kolom belum diubah/tidak sesuai, tampilkan semua data sebagai cadangan aman agar tidak error
            st.warning(f"Kolom pemisah '{nama_kolom_pemisah}' tidak ditemukan di spreadsheet. Menampilkan seluruh data.")
            st.dataframe(df_asset, use_container_width=True, hide_index=True)
            st.info("💡 **Tips:** Silakan buka file `app.py`, lalu ganti variabel `nama_kolom_pemisah = 'Jenis Asset'` sesuai nama kolom asli di Google Sheets Anda.")
            
    else:
        st.caption("Lembar kerja 'data Asset' kosong atau tidak ditemukan.")


# --- MENU 5: TAB DATA KPI ---
def halaman_data_kpi():
    st.title("📈 Network Performance Indicator (data KPI)")
    st.caption("Indikator performa kualitas jaringan telekomunikasi regional.")
    df_kpi = ambil_data_sheet("data KPI")
    if not df_kpi.empty:
        st.dataframe(df_kpi, use_container_width=True, hide_index=True)
    else:
        st.caption("Lembar kerja 'data KPI' kosong atau tidak ditemukan.")

# --- MENU 6: TAB DATA OPERATIONAL ---
def halaman_data_operational():
    st.title("⚙️ Network Operations Center Data (data Operational)")
    st.caption("Log pemantauan operasional lapangan harian dan utilitas kapasitas server.")
    df_ops = ambil_data_sheet("data Operational")
    if not df_ops.empty:
        st.dataframe(df_ops, use_container_width=True, hide_index=True)
    else:
        st.caption("Lembar kerja 'data Operational' kosong atau tidak ditemukan.")

# --- MENU 7: TAB DATA PJB AGING ---
def halaman_data_pjb():
    st.title("⏳ PJB Aging & Outstanding Log (data PJB aging)")
    st.caption("Pelacakan berkas, dokumen kontrak, atau aging proses administrasi finansial proyek.")
    df_pjb = ambil_data_sheet("data PJB aging")
    if not df_pjb.empty:
        st.dataframe(df_pjb, use_container_width=True, hide_index=True)
    else:
        st.caption("Lembar kerja 'data PJB aging' kosong atau tidak ditemukan.")

# --- MENU 8: TAB MONITORING MBP / PROGRESS MATELINE PLACEHOLDER ---
def halaman_monitoring_mbp():
    st.title("📡 Monitoring MBP & Progress Mateline Management")
    st.caption("Wadah monitoring ketersediaan daya cadangan (Mobile Backup Power) dan logistik pasokan material.")
    
    # Membaca data jika di masa depan Anda menambahkan tab ini ke spreadsheet utama Anda
    df_mbp = ambil_data_sheet("Monitoring MBP")
    if not df_mbp.empty:
        st.dataframe(df_mbp, use_container_width=True, hide_index=True)
    else:
        st.info("💡 Struktur siap pakai. Data live otomatis termuat di halaman ini apabila Anda menambahkan tab baru bernama 'Monitoring MBP' ke Google Sheets Anda.")

# ==========================================
# 4. ROUTER EKSEKUSI HALAMAN
# ==========================================
if st.session_state.active_menu == "VARCOST":
    halaman_varcost()
elif st.session_state.active_menu == "DATA_PM":
    halaman_data_pm()
elif st.session_state.active_menu == "DATA_PROJECT":
    halaman_data_project()
elif st.session_state.active_menu == "DATA_ASSET":
    halaman_data_asset()
elif st.session_state.active_menu == "DATA_KPI":
    halaman_data_kpi()
elif st.session_state.active_menu == "DATA_OPERATIONAL":
    halaman_data_operational()
elif st.session_state.active_menu == "DATA_PJB":
    halaman_data_pjb()
elif st.session_state.active_menu == "MONITORING_MBP":
    halaman_monitoring_mbp()
