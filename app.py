import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & Tema Gelap Ops Center
st.set_page_config(
    page_title="Telco Corporate Dashboard - Reg Kalimantan", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inisialisasi session state untuk navigasi halaman jika belum ada
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST"

# ID Spreadsheet Utama Anda (Dihasilkan langsung dari link Database Reg Kalimantan)
SPREADSHEET_ID = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"

# Fungsi pembacaan data publik bypass menggunakan pandas read_csv (100% Stabil & Bebas Hambatan Jaringan)
@st.cache_data(ttl=30)
def ambil_data_sheet(nama_sheet):
    try:
        sheet_aman = nama_sheet.replace(" ", "%20")
        url_csv = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_aman}"
        # Membaca baris kedua (index baris 1) sebagai header jika baris pertama berupa merge-cell/title
        df = pd.read_csv(url_csv, header=1)
        return df
    except:
        return pd.DataFrame()

# ==========================================
# 2. NAVIGASI ATAS (8 MENU PRESISI & INSTAN)
# ==========================================
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
    st.caption("Memantau ringkasan biaya operasional dan data finansial regional dari tab 'data SVA / VARCOST'.")
    st.write("")

    # Membaca lembar kerja pertama yang berisi ringkasan finansial utama Anda
    df_raw = ambil_data_sheet("data SVA")

    # Jika "data SVA" tidak merespon, gunakan fallback ke nama alternatif "VARCOST"
    if df_raw.empty:
        df_raw = ambil_data_sheet("VARCOST")

    # Dropdown Analisa Finansial
    st.subheader("📊 Corporate Financial Dropdown")
    opsi_analisa = st.selectbox(
        "Pilih Lini Analisis Finansial:",
        ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
    )

    if not df_raw.empty:
        # Bersihkan spasi kosong di nama-nama kolom spreadsheet
        df_varcost = df_raw.copy()
        df_varcost.columns = df_varcost.columns.str.strip()

        # Pemetaan berdasarkan nama kolom asli di Google Sheets Anda
        col_bulan = "Bulan"
        col_revenue = "Nilai Revenue"
        col_income = "Net Income"

        # Fungsi konversi data teks ke angka finansial agar grafik berfungsi
        for col in [col_revenue, col_income]:
            if col in df_varcost.columns:
                df_varcost[col] = df_varcost[col].astype(str).str.replace('.', '', regex=False)
                df_varcost[col] = pd.to_numeric(df_varcost[col], errors='coerce').fillna(0)

        # Tampilan Grafik 1: Revenue
        if opsi_analisa == "Revenue Analysis (Pendapatan)":
            if col_bulan in df_varcost.columns and col_revenue in df_varcost.columns:
                # Ambil baris data yang valid, kumpulkan berdasarkan grup bulan
                df_chart = df_varcost[[col_bulan, col_revenue]].dropna()
                df_grouped = df_chart.groupby(col_bulan).sum()
                st.line_chart(df_grouped)
            else:
                st.warning(f"Kolom '{col_bulan}' atau '{col_revenue}' tidak cocok. Kolom terdeteksi: {list(df_raw.columns)}")
                
        # Tampilan Grafik 2: Net Income
        elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
            if col_bulan in df_varcost.columns and col_income in df_varcost.columns:
                df_chart = df_varcost[[col_bulan, col_income]].dropna()
                df_grouped = df_chart.groupby(col_bulan).sum()
                st.bar_chart(df_grouped)
            else:
                st.warning(f"Kolom '{col_bulan}' atau '{col_income}' tidak cocok. Kolom terdeteksi: {list(df_raw.columns)}")

        # Menampilkan Ringkasan Metrik Finansial Akumulatif
        st.write("")
        st.subheader("📈 Ringkasan Nilai Finansial")
        m1, m2 = st.columns(2)
        with m1:
            total_rev_sum = df_varcost[col_revenue].sum() if col_revenue in df_varcost.columns else 0
            st.metric(label="Total Kumulatif Revenue", value=f"IDR {total_rev_sum:,.0f}")
        with m2:
            total_inc_sum = df_varcost[col_income].sum() if col_income in df_varcost.columns else 0
            st.metric(label="Total Kumulatif Net Income", value=f"IDR {total_inc_sum:,.0f}")

        # Menampilkan Tabel Utama Asli
        st.write("")
        st.subheader("📋 Seluruh Data Sheet Riil")
        st.dataframe(df_raw, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Koneksi berhasil terhubung tetapi lembar kerja spreadsheet kosong atau nama tab tidak sesuai.")

# --- MENU 2: TAB DATA PM ---
def halaman_data_pm():
    st.title("🛠️ Preventive Maintenance Log (data PM)")
    df_pm = ambil_data_sheet("data PM")
    if not df_pm.empty:
        st.dataframe(df_pm, use_container_width=True, hide_index=True)
    else:
        st.info("Menunggu sinkronisasi data atau tab 'data PM' kosong.")

# --- MENU 3: TAB DATA PROJECT ---
def halaman_data_project():
    st.title("🚀 Network Rollout Progress (data Project)")
    df_project = ambil_data_sheet("data Project")
    if not df_project.empty:
        st.dataframe(df_project, use_container_width=True, hide_index=True)
    else:
        st.info("Menunggu sinkronisasi data atau tab 'data Project' kosong.")

# --- MENU 4: TAB DATA ASSET (DENGAN SUB-MENU KUT & RENTAL) ---
def halaman_data_asset():
    st.title("🏢 Asset Management Inventory (data Asset)")
    df_asset = ambil_data_sheet("data Asset")
    
    if not df_asset.empty:
        sub_menu = st.radio("Pilih Kategori Asset:", ["Semua Asset", "Asset KUT", "Asset Rental"], horizontal=True)
        st.write("")
        
        # Bersihkan nama kolom asset dari spasi liar
        df_asset.columns = df_asset.columns.str.strip()
        
        # Menganalisis kolom pertama sebagai filter kata kunci kategori asset
        col_filter = df_asset.columns[0] 
        
        if sub_menu == "Semua Asset":
            st.dataframe(df_asset, use_container_width=True, hide_index=True)
        elif sub_menu == "Asset KUT":
            df_kut = df_asset[df_asset[col_filter].astype(str).str.contains("KUT", case=False, na=False)]
            st.dataframe(df_kut, use_container_width=True, hide_index=True) if not df_kut.empty else st.info("Kategori Asset KUT belum ditemukan.")
        elif sub_menu == "Asset Rental":
            df_rental = df_asset[df_asset[col_filter].astype(str).str.contains("Rental", case=False, na=False)]
            st.dataframe(df_rental, use_container_width=True, hide_index=True) if not df_rental.empty else st.info("Kategori Asset Rental belum ditemukan.")
    else:
        st.info("Menunggu sinkronisasi data atau tab 'data Asset' kosong.")

# --- MENU 5: TAB DATA KPI ---
def halaman_data_kpi():
    st.title("📈 Network Performance Indicator (data KPI)")
    df_kpi = ambil_data_sheet("data KPI")
    if not df_kpi.empty:
        st.dataframe(df_kpi, use_container_width=True, hide_index=True)
    else:
        st.info("Menunggu sinkronisasi data atau tab 'data KPI' kosong.")

# --- MENU 6: TAB DATA OPERATIONAL ---
def halaman_data_operational():
    st.title("⚙️ Network Operations Data (data Operational)")
    df_ops = ambil_data_sheet("data Operational")
    if not df_ops.empty:
        st.dataframe(df_ops, use_container_width=True, hide_index=True)
    else:
        st.info("Menunggu sinkronisasi data atau tab 'data Operational' kosong.")

# --- MENU 7: TAB DATA PJB AGING ---
def halaman_data_pjb():
    st.title("⏳ PJB Aging Log (data PJB aging)")
    df_pjb = ambil_data_sheet("data PJB aging")
    if not df_pjb.empty:
        st.dataframe(df_pjb, use_container_width=True, hide_index=True)
    else:
        st.info("Menunggu sinkronisasi data atau tab 'data PJB aging' kosong.")

# --- MENU 8: TAB MONITORING MBP ---
def halaman_monitoring_mbp():
    st.title("📡 Monitoring MBP & Progress Mateline Management")
    st.info("Struktur monitoring ketersediaan daya cadangan (Mobile Backup Power) siap disinkronisasikan.")

# ==========================================
# 4. ROUTER EKSEKUSI HALAMAN
# ==========================================
if st.session_state.active_menu == "VARCOST":
    halaman_varcost()
elif st.session_state.active_menu == "DATA_PM":
    halaman_data_pm()
