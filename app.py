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

# ID Spreadsheet Utama (Dihasilkan dari link publik Database Reg Kalimantan Anda)
SPREADSHEET_ID = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"

# Fungsi pembacaan data publik bypass yang aman dari pemblokiran DNS
@st.cache_data(ttl=60) # Cache otomatis kedaluwarsa setiap 60 detik
def ambil_data_sheet(nama_sheet):
    try:
        sheet_aman = nama_sheet.replace(" ", "%20")
        url_csv = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_aman}"
        df = pd.read_csv(url_csv)
        return df
    except:
        return pd.DataFrame()

# ==========================================
# 2. NAVIGASI ATAS & TOMBOL REFRESH INSTAN
# ==========================================
# Membagi kolom menjadi 9 bagian (8 untuk menu, 1 untuk tombol refresh)
col1, col2, col3, col4, col5, col6, col7, col8, col_ref = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1.2])

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

# 🔄 TOMBOL UTAMA REFRESH ALL DATA
with col_ref:
    if st.button("🔄\n\nREFRESH DATA", use_container_width=True, key="btn_refresh_all", type="primary"):
        st.cache_data.clear() # Menghapus seluruh cache memori Streamlit seketika
        st.toast("Memperbarui seluruh data langsung dari Google Sheets...", icon="🔄")
        st.rerun()

st.markdown("---")

# ==========================================
# 3. KONTEN HALAMAN (RESOURCE LIVE GOOGLE SHEETS)
# ==========================================

# --- MENU 1: TAB VARCOST (MENGAMBIL GRAFIK DARI SHEET data SVA) ---
def halaman_varcost():
    st.title("🌐 Telecom Variable Cost Analysis")
    st.caption("Memantau ringkasan biaya operasional wilayah Kalimantan langsung dari Google Sheets.")
    st.write("")

    # Dropdown Analisa Finansial
    st.subheader("📊 Corporate Financial Dropdown")
    opsi_analisa = st.selectbox(
        "Pilih Lini Analisis Finansial:",
        ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
    )

    # Memuat data dari sheet 'data SVA' untuk visualisasi grafik finansial
    df_sva = ambil_data_sheet("data SVA")

    if not df_sva.empty:
        try:
            # Mengambil nama kolom asli berdasarkan urutan alfabet di spreadsheet Anda (F=5, G=6, T=19)
            nama_col_revenue = df_sva.columns[5]   # Kolom F
            nama_col_bulan = df_sva.columns[6]     # Kolom G
            nama_col_income = df_sva.columns[19]   # Kolom T

            # Tampilan Grafik 1: Revenue
            if opsi_analisa == "Revenue Analysis (Pendapatan)":
                st.info(f"📈 **Tren Revenue Bulanan (Sumber: data SVA - Kolom {nama_col_revenue})**")
                df_chart = df_sva[[nama_col_bulan, nama_col_revenue]].dropna()
                df_chart = df_chart.set_index(nama_col_bulan)
                st.line_chart(df_chart)
                
                # Metrik nilai terkini (baris terakhir)
                val_rev = df_sva[nama_col_revenue].iloc[-1]
                st.metric(label="Revenue Periode Terakhir", value=str(val_rev))

            # Tampilan Grafik 2: Net Income
            elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
                st.success(f"💰 **Tren Net Income Bulanan (Sumber: data SVA - Kolom {nama_col_income})**")
                df_chart = df_sva[[nama_col_bulan, nama_col_income]].dropna()
                df_chart = df_chart.set_index(nama_col_bulan)
                st.bar_chart(df_chart)
                
                # Metrik nilai terkini (baris terakhir)
                val_inc = df_sva[nama_col_income].iloc[-1]
                st.metric(label="Net Income Periode Terakhir", value=str(val_inc))

        except IndexError:
            st.warning("⚠️ Struktur kolom pada sheet 'data SVA' kurang dari 20 kolom (Kolom T tidak terjangkau). Menampilkan data apa adanya.")
    else:
        st.info("💡 Grafik finansial akan muncul secara otomatis setelah tab 'data SVA' tersinkronisasi.")

    st.markdown("---")

    # Menampilkan Tabel Utama dari sheet VARCOST asli di bagian bawah
    st.subheader("📋 Data Sheet Riil: VARCOST")
    df_varcost = ambil_data_sheet("VARCOST")
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True, hide_index=True)
    else:
        st.warning("Data tabel 'VARCOST' kosong atau sedang memuat. Coba klik tombol **REFRESH DATA** di pojok kanan atas.")

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

# --- MENU 4: TAB DATA ASSET ---
def halaman_data_asset():
    st.title("🏢 Asset Management Inventory (data Asset)")
    df_asset = ambil_data_sheet("data Asset")
    if not df_asset.empty:
        st.dataframe(df_asset, use_container_width=True, hide_index=True)
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
    st.info("Struktur penampung siap pakai untuk memantau modul operasional lapangan tambahan.")

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
