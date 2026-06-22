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

# Tautan Spreadsheet Utama Anda (Database Reg Kalimantan)
URL_SPREADSHEET = "https://google.com"

# Fungsi membaca data dengan proteksi layar kosong
@st.cache_data(ttl=30) # Segarkan cache lebih cepat (30 detik) jika masih tahap testing
def ambil_data_sheet(nama_sheet):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Menambahkan argumen pembacaan langsung dari URL publik tanpa hambatan
        df = conn.read(spreadsheet=URL_SPREADSHEET, worksheet=nama_sheet)
        if df is not None:
            return df
        return pd.DataFrame()
    except Exception as e:
        # Jika gagal, kembalikan DataFrame kosong agar program di bawahnya tetap tereksekusi
        return pd.DataFrame()

# ==========================================
# 2. NAVIGASI ATAS (8 MENU PRESISI & INSTAN)
# ==========================================
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    if st.button("💰\n\nVARCOST", use_container_width=True, key="btn_varcost"):
        st.session_state.active_menu = "VARCOST"
        st.grid = None # reset state
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

# --- MENU 1: TAB VARCOST (VERSI PERBAIKAN KOLOM & GRAFIK) ---
def halaman_varcost():
    st.title("🌐 Telecom Variable Cost Analysis")
    st.caption("Memantau ringkasan biaya operasional dan data finansial regional dari tab 'VARCOST'.")
    st.write("")

    # 1. Tarik data mentah
    df_raw = ambil_data_sheet("VARCOST")

    if not df_raw.empty:
        # 2. Pembersihan otomatis nama kolom (menghapus spasi & huruf kecil semua)
        # Langkah ini menjamin kode tidak akan eror meski di Google Sheets tertulis 'revenue ', 'Revenue', atau 'REVENUE'
        df_varcost = df_raw.copy()
        df_varcost.columns = df_varcost.columns.str.strip().str.lower()

        # Dropdown Analisa Finansial
        st.subheader("📊 Corporate Financial Dropdown")
        opsi_analisa = st.selectbox(
            "Pilih Lini Analisis Finansial:",
            ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
        )

        # Pemetaan nama kolom setelah dikecilkan otomatis
        col_bulan = "bulan"
        col_revenue = "revenue"
        col_income = "net income"

        # Tampilan Grafik 1: Revenue
        if opsi_analisa == "Revenue Analysis (Pendapatan)":
            if col_bulan in df_varcost.columns and col_revenue in df_varcost.columns:
                # Membuat data frame khusus grafik dan membersihkan baris kosong (dropna)
                df_chart = df_varcost[[col_bulan, col_revenue]].dropna()
                df_chart = df_chart.set_index(col_bulan)
                st.line_chart(df_chart)
            else:
                st.warning(f"⚠️ Kolom '{col_bulan}' atau '{col_revenue}' tidak terdeteksi. Kolom yang ditemukan di sheet Anda: {list(df_raw.columns)}")
                
        # Tampilan Grafik 2: Net Income
        elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
            if col_bulan in df_varcost.columns and col_income in df_varcost.columns:
                df_chart = df_varcost[[col_bulan, col_income]].dropna()
                df_chart = df_chart.set_index(col_bulan)
                st.bar_chart(df_chart)
            else:
                st.warning(f"⚠️ Kolom '{col_bulan}' atau '{col_income}' tidak terdeteksi. Kolom yang ditemukan di sheet Anda: {list(df_raw.columns)}")

        # Menampilkan Ringkasan Metrik Terkini (Mengambil baris terbawah data)
        st.write("")
        st.subheader("📈 Ringkasan Nilai Terkini")
        m1, m2 = st.columns(2)
        
        with m1:
            val_rev = df_raw[df_raw.columns[df_varcost.columns == col_revenue]].iloc[-1].values[0] if col_revenue in df_varcost.columns else "-"
            st.metric(label="Revenue Terakhir", value=str(val_rev))
        with m2:
            val_inc = df_raw[df_raw.columns[df_varcost.columns == col_income]].iloc[-1].values[0] if col_income in df_varcost.columns else "-"
            st.metric(label="Net Income Terakhir", value=str(val_inc))

        # Menampilkan Tabel Utama Asli
        st.write("")
        st.subheader("📋 Data Sheet Riil: VARCOST")
        st.dataframe(df_raw, use_container_width=True, hide_index=True)

    else:
        st.warning("⚠️ Data Utama gagal ditarik dari Google Sheets atau tab 'VARCOST' kosong.")
        st.info("Pastikan spreadsheet Anda sudah diatur ke akses publik: **'Anyone with the link can view'**.")

# --- MENU 2: TAB DATA PM ---
def halaman_data_pm():
    st.title("🛠️ Preventive Maintenance Log (data PM)")
    st.caption("Memantau rekam aktivitas pemeliharaan infrastruktur secara berkala.")
    df_pm = ambil_data_sheet("data PM")
    if not df_pm.empty:
        st.dataframe(df_pm, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data untuk ditampilkan atau tab 'data PM' kosong.")

# --- MENU 3: TAB DATA PROJECT ---
def halaman_data_project():
    st.title("🚀 Network Rollout & Deployment Progress (data Project)")
    st.caption("Status pembangunan jaringan, site baru, dan integrasi sistem telekomunikasi.")
    df_project = ambil_data_sheet("data Project")
    if not df_project.empty:
        st.dataframe(df_project, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data untuk ditampilkan atau tab 'data Project' kosong.")

# --- MENU 4: TAB DATA ASSET ---
def halaman_data_asset():
    st.title("🏢 Asset Management Inventory (data Asset)")
    st.caption("Manajemen aset perangkat core, transmisi, menara (tower), dan fasilitas penunjang.")
    
    df_asset = ambil_data_sheet("data Asset")

    if not df_asset.empty:
        sub_menu = st.radio("Pilih Kategori Kategori Asset:", ["Semua Asset", "Asset KUT", "Asset Rental"], horizontal=True)
        nama_kolom_pemisah = "Jenis Asset" 

        if nama_kolom_pemisah in df_asset.columns:
            if sub_menu == "Semua Asset":
                st.dataframe(df_asset, use_container_width=True, hide_index=True)
            elif sub_menu == "Asset KUT":
                df_kut = df_asset[df_asset[nama_kolom_pemisah].astype(str).str.contains("KUT", case=False, na=False)]
                st.dataframe(df_kut, use_container_width=True, hide_index=True) if not df_kut.empty else st.info("Kategori KUT Kosong.")
            elif sub_menu == "Asset Rental":
                df_rental = df_asset[df_asset[nama_kolom_pemisah].astype(str).str.contains("Rental", case=False, na=False)]
                st.dataframe(df_rental, use_container_width=True, hide_index=True) if not df_rental.empty else st.info("Kategori Rental Kosong.")
        else:
            st.dataframe(df_asset, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data untuk ditampilkan atau tab 'data Asset' kosong.")

# --- MENU 5: TAB DATA KPI ---
def halaman_data_kpi():
    st.title("📈 Network Performance Indicator (data KPI)")
    df_kpi = ambil_data_sheet("data KPI")
    if not df_kpi.empty:
        st.dataframe(df_kpi, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data untuk ditampilkan atau tab 'data KPI' kosong.")

# --- MENU 6: TAB DATA OPERATIONAL ---
def halaman_data_operational():
    st.title("⚙️ Network Operations Center Data (data Operational)")
    df_ops = ambil_data_sheet("data Operational")
    if not df_ops.empty:
        st.dataframe(df_ops, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data untuk ditampilkan atau tab 'data Operational' kosong.")

# --- MENU 7: TAB DATA PJB AGING ---
def halaman_data_pjb():
    st.title("⏳ PJB Aging & Outstanding Log (data PJB aging)")
    df_pjb = ambil_data_sheet("data PJB aging")
    if not df_pjb.empty:
        st.dataframe(df_pjb, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada data untuk ditampilkan atau tab 'data PJB aging' kosong.")

# --- MENU 8: TAB MONITORING MBP ---
def halaman_monitoring_mbp():
    st.title("📡 Monitoring MBP & Progress Mateline Management")
    st.info("💡 Data live otomatis termuat di halaman ini apabila Anda menambahkan tab baru bernama 'Monitoring MBP' ke Google Sheets Anda.")

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
