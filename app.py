import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Konfigurasi Halaman & Tema Gelap ala Telco Ops Center
st.set_page_config(
    page_title="Telco Corporate Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inisialisasi session state untuk navigasi halaman jika belum ada
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST"

# Tautan Spreadsheet Utama Anda (Database Reg Kalimantan)
URL_SPREADSHEET = "https://google.com"

# Fungsi resmi menggunakan st.connection (Aman dari pemblokiran DNS server)
@st.cache_data(ttl=60)
def ambil_data_sheet(nama_sheet):
    try:
        # Menggunakan koneksi bawaan Streamlit Cloud yang terotentikasi stabil
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL_SPREADSHEET, worksheet=nama_sheet)
        return df
    except Exception as e:
        st.error(f"Gagal memuat sheet '{nama_sheet}': {e}")
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
    if st.button("📈\n\nKPI", use_container_width=True, key="btn_kpi"):
        st.session_state.active_menu = "KPI"
        st.rerun()
with col3:
    if st.button("🛠️\n\nMAINTENANCE", use_container_width=True, key="btn_maint"):
        st.session_state.active_menu = "MAINTENANCE"
        st.rerun()
with col4:
    if st.button("🏢\n\nASSET", use_container_width=True, key="btn_asset"):
        st.session_state.active_menu = "ASSET"
        st.rerun()
with col5:
    if st.button("🚀\n\nPROJECT", use_container_width=True, key="btn_project"):
        st.session_state.active_menu = "PROJECT"
        st.rerun()
with col6:
    if st.button("⚙️\n\nOPERATIONAL", use_container_width=True, key="btn_operational"):
        st.session_state.active_menu = "OPERATIONAL"
        st.rerun()
with col7:
    if st.button("📡\n\nMONITORING MBP", use_container_width=True, key="btn_mbp"):
        st.session_state.active_menu = "MONITORING_MBP"
        st.rerun()
with col8:
    if st.button("📋\n\nPROGRESS MATELINE", use_container_width=True, key="btn_mateline"):
        st.session_state.active_menu = "PROGRESS_MATELINE"
        st.rerun()

st.markdown("---")

# ==========================================
# 3. KONTEN HALAMAN (KONEKSI LIVE GOOGLE SHEETS)
# ==========================================

# --- HALAMAN UTAMA (VARCOST TELCO + DROPDOWN ANALISA FINANSIAL) ---
def halaman_varcost():
    st.title("🌐 Telecom Variable Cost & Financial Analysis")
    st.caption("Memantau data keuangan dan fluktuasi biaya operasional wilayah Kalimantan langsung dari Google Sheets.")
    st.write("")

    df_varcost = ambil_data_sheet("Monitoring Varcost")

    # Dropdown Analisa Finansial (Revenue & Income)
    st.subheader("📊 Corporate Financial Analysis")
    opsi_analisa = st.selectbox(
        "Pilih Metrik Analisis Finansial:",
        ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
    )

    if opsi_analisa == "Revenue Analysis (Pendapatan)":
        r1, r2 = st.columns(2)
        with r1:
            st.info("📈 **Tren Pendapatan Terbaca**")
            if not df_varcost.empty and 'Bulan' in df_varcost.columns and 'Revenue' in df_varcost.columns:
                data_rev = df_varcost.set_index('Bulan')[['Revenue']]
                st.line_chart(data_rev)
            else:
                st.warning("Menunggu ketersediaan data dengan nama kolom 'Bulan' dan 'Revenue' di sheet Anda.")
        with r2:
            total_rev = df_varcost['Revenue'].iloc[-1] if not df_varcost.empty and 'Revenue' in df_varcost.columns else "-"
            st.metric(label="Total Revenue Terkini", value=str(total_rev))

    elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
        i1, i2 = st.columns(2)
        with i1:
            st.success("💰 **Tren Laba Bersih**")
            if not df_varcost.empty and 'Bulan' in df_varcost.columns and 'Net Income' in df_varcost.columns:
                data_inc = df_varcost.set_index('Bulan')[['Net Income']]
                st.bar_chart(data_inc)
            else:
                st.warning("Menunggu ketersediaan data dengan nama kolom 'Bulan' dan 'Net Income' di sheet Anda.")
        with i2:
            npm = df_varcost['NPM'].iloc[-1] if not df_varcost.empty and 'NPM' in df_varcost.columns else "-"
            st.metric(label="Net Profit Margin (NPM)", value=str(npm))

    st.markdown("---")

    st.subheader("📋 Seluruh Baris Data Realtime 'Monitoring Varcost'")
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True, hide_index=True)
    else:
        st.caption("Lembar kerja 'Monitoring Varcost' kosong atau tidak ditemukan.")

# --- HALAMAN MENU LAINNYA SESUAI TAB SPREADSHEET ---
def halaman_kpi():
    st.title("📈 Telecom Network KPI")
    df_kpi = ambil_data_sheet("data KPI")
    if not df_kpi.empty:
        st.dataframe(df_kpi, use_container_width=True, hide_index=True)

def halaman_maintenance():
    st.title("🛠️ Preventive & Corrective Maintenance")
    df_pm = ambil_data_sheet("data PM")
    if not df_pm.empty:
        st.dataframe(df_pm, use_container_width=True, hide_index=True)

def halaman_asset():
    st.title("🏢 Telecom Asset Inventory")
    df_asset = ambil_data_sheet("data Asset")
    if not df_asset.empty:
        st.dataframe(df_asset, use_container_width=True, hide_index=True)

def halaman_project():
    st.title("🚀 Network Rollout & Project Deployment")
    df_project = ambil_data_sheet("data Project")
    if not df_project.empty:
        st.dataframe(df_project, use_container_width=True, hide_index=True)

def halaman_operational():
    st.title("⚙️ Network Operations Center (NOC)")
    df_ops = ambil_data_sheet("data Operational")
    if not df_ops.empty:
        st.dataframe(df_ops, use_container_width=True, hide_index=True)

def halaman_monitoring_mbp():
    st.title("📡 Monitoring MBP (Mobile Backup Power)")
    df_mbp = ambil_data_sheet("Monitoring MBP")
    if not df_mbp.empty:
        st.dataframe(df_mbp, use_container_width=True, hide_index=True)

def halaman_progress_mateline():
    st.title("📋 Progress Mateline & Material Management")
    df_mateline = ambil_data_sheet("Progress Mateline")
    if not df_mateline.empty:
        st.dataframe(df_mateline, use_container_width=True, hide_index=True)

# ==========================================
# 4. ROUTER EKSEKUSI HALAMAN
# ==========================================
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
elif st.session_state.active_menu == "MONITORING_MBP":
    halaman_monitoring_mbp()
elif st.session_state.active_menu == "PROGRESS_MATELINE":
    halaman_progress_mateline()
