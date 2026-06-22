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

# ID Spreadsheet Utama Anda (Dihasilkan langsung dari link Database Reg Kalimantan Anda)
SPREADSHEET_ID = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"

# Fungsi pembacaan data publik bypass yang 100% aman dari error macet layar kosong
@st.cache_data(ttl=15) # Refresh cepat 15 detik selama pengujian
def ambil_data_sheet(nama_sheet):
    try:
        # Mengonversi nama sheet agar aman dibaca oleh URL Google Docs API
        sheet_aman = nama_sheet.replace(" ", "%20")
        url_csv = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_aman}"
        df = pd.read_csv(url_csv)
        return df
    except:
        # Mengembalikan DataFrame kosong buatan jika koneksi dari cloud ke Google diblokir
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
    st.caption("Memantau ringkasan biaya operasional dan data finansial regional dari tab 'VARCOST'.")
    st.write("")

    # Dropdown Analisa Finansial (Tetap muncul di layar apa pun kondisi datanya)
    st.subheader("📊 Corporate Financial Dropdown")
    opsi_analisa = st.selectbox(
        "Pilih Lini Analisis Finansial:",
        ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
    )

    df_raw = ambil_data_sheet("VARCOST")

    if not df_raw.empty:
        # Bersihkan nama kolom dari spasi liar dan buat menjadi huruf kecil semua
        df_varcost = df_raw.copy()
        df_varcost.columns = df_varcost.columns.str.strip().str.lower()

        col_bulan = "bulan"
        col_revenue = "revenue"
        col_income = "net income"

        # Tampilan Grafik
        if opsi_analisa == "Revenue Analysis (Pendapatan)":
            if col_bulan in df_varcost.columns and col_revenue in df_varcost.columns:
                st.line_chart(df_varcost[[col_bulan, col_revenue]].dropna().set_index(col_bulan))
            else:
                st.info("💡 Grafik pendapatan akan muncul jika kolom 'Bulan' dan 'Revenue' tersedia di dalam sheet.")
        elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
            if col_bulan in df_varcost.columns and col_income in df_varcost.columns:
                st.bar_chart(df_varcost[[col_bulan, col_income]].dropna().set_index(col_bulan))
            else:
                st.info("💡 Grafik laba bersih akan muncul jika kolom 'Bulan' dan 'Net Income' tersedia di dalam sheet.")

        # Menampilkan Ringkasan Metrik
        st.write("")
        st.subheader("📈 Ringkasan Nilai Terkini")
        m1, m2 = st.columns(2)
        with m1:
            val_rev = df_raw[df_raw.columns[df_varcost.columns == col_revenue]].iloc[-1].values if col_revenue in df_varcost.columns else "-"
            st.metric(label="Revenue Terakhir", value=str(val_rev))
        with m2:
            val_inc = df_raw[df_raw.columns[df_varcost.columns == col_income]].iloc[-1].values if col_income in df_varcost.columns else "-"
            st.metric(label="Net Income Terakhir", value=str(val_inc))

        # Menampilkan Tabel Utama Asli
        st.write("")
        st.subheader("📋 Data Sheet Riil: VARCOST")
        st.dataframe(df_raw, use_container_width=True, hide_index=True)
    else:
        # JIKA PULL DATA GAGAL, LAYAR TIDAK AKAN BLANK HITAM LAGI
        st.error("❌ Streamlit Cloud Gagal Menghubungi Google Sheets Anda!")
        st.warning("⚠️ **Penyebab Utama:** Hak akses berbagi pada link Google Sheets Anda masih terkunci (*Restricted*).")
        st.info("👉 **Cara Mengatasi Seketika:** Buka spreadsheet Anda, klik tombol **Share** di pojok kanan atas, lalu ubah opsi General Access dari *Restricted* menjadi **'Anyone with the link can view'** (Siapa saja yang memiliki link dapat melihat).")

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
    st.info("Struktur penampung siap pakai untuk tab 'Monitoring MBP'.")

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
