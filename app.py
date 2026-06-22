import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import urllib.parse

# 1. Konfigurasi Halaman & Tema Gelap Ops Center
st.set_page_config(
    page_title="Telco Corporate Dashboard - Reg Kalimantan", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inisialisasi session state untuk navigasi halaman jika belum ada
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST"
if "play_sound" not in st.session_state:
    st.session_state.play_sound = False

# ID Spreadsheet Utama Anda (Dihasilkan dari link publik Database Reg Kalimantan Anda)
SPREADSHEET_ID = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"

# 🔊 FUNGSI EFEK SUARA KLIK
def putar_suara_klik():
    sound_url = "https://soundjay.com"
    html_code = f"""
    <audio autoplay hidden><source src="{sound_url}" type="audio/mp3"></audio>
    """
    components.html(html_code, height=0, width=0)

if st.session_state.play_sound:
    putar_suara_klik()
    st.session_state.play_sound = False

# 🌐 FUNGSI UTAMA: Membaca Google Sheet via Direct Web Export (Anti-Gagal setelah Publish to Web)
@st.cache_data(ttl=5) # Segarkan data otomatis dalam 5 detik
def ambil_data_sheet(nama_sheet):
    try:
        sheet_aman = urllib.parse.quote(nama_sheet)
        url_csv = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_aman}"
        df = pd.read_csv(url_csv)
        return df
    except Exception as e:
        return pd.DataFrame()

# ==========================================
# 2. NAVIGASI ATAS & TOMBOL REFRESH INSTAN
# ==========================================
col1, col2, col3, col4, col5, col6, col7, col8, col_ref = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1.2])

with col1:
    if st.button("💰\n\nVARCOST", use_container_width=True, key="btn_varcost"):
        st.session_state.active_menu = "VARCOST"; st.session_state.play_sound = True; st.rerun()
with col2:
    if st.button("🛠️\n\nDATA PM", use_container_width=True, key="btn_pm"):
        st.session_state.active_menu = "DATA_PM"; st.session_state.play_sound = True; st.rerun()
with col3:
    if st.button("🚀\n\nDATA PROJECT", use_container_width=True, key="btn_project"):
        st.session_state.active_menu = "DATA_PROJECT"; st.session_state.play_sound = True; st.rerun()
with col4:
    if st.button("🏢\n\nDATA ASSET", use_container_width=True, key="btn_asset"):
        st.session_state.active_menu = "DATA_ASSET"; st.session_state.play_sound = True; st.rerun()
with col5:
    if st.button("📈\n\nDATA KPI", use_container_width=True, key="btn_kpi"):
        st.session_state.active_menu = "DATA_KPI"; st.session_state.play_sound = True; st.rerun()
with col6:
    if st.button("⚙️\n\nDATA OPERATIONAL", use_container_width=True, key="btn_operational"):
        st.session_state.active_menu = "DATA_OPERATIONAL"; st.session_state.play_sound = True; st.rerun()
with col7:
    if st.button("⏳\n\nDATA PJB AGING", use_container_width=True, key="btn_pjb"):
        st.session_state.active_menu = "DATA_PJB"; st.session_state.play_sound = True; st.rerun()
with col8:
    if st.button("📡\n\nMONITORING MBP", use_container_width=True, key="btn_mbp"):
        st.session_state.active_menu = "MONITORING_MBP"; st.session_state.play_sound = True; st.rerun()
with col_ref:
    if st.button("🔄\n\nREFRESH DATA", use_container_width=True, key="btn_refresh_all", type="primary"):
        st.cache_data.clear(); st.session_state.play_sound = True
        st.toast("Memperbarui seluruh data dari Google Sheets...", icon="🔄")
        st.rerun()

st.markdown("---")

# ==========================================
# 3. KONTEN HALAMAN (RESOURCE LIVE)
# ==========================================

def halaman_varcost():
    st.title("🌐 Telecom Variable Cost Analysis")
    st.caption("Memantau ringkasan biaya operasional wilayah Kalimantan langsung dari Google Sheets.")
    st.write("")

    st.subheader("📊 Corporate Financial Dropdown")
    opsi_analisa = st.selectbox(
        "Pilih Lini Analisis Finansial:",
        ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
    )

    # Memuat data live dari sheet 'data SVA'
    df_sva = ambil_data_sheet("data SVA")

    if not df_sva.empty:
        try:
            # 💡 FITUR BARU ANTI-ERROR: Ambil nama asli kolom berdasarkan urutan urutan fisiknya di Excel
            # Kolom F (Revenue) = Indeks ke-5
            # Kolom G (Bulan) = Indeks ke-6
            # Kolom T (Net Income) = Indeks ke-19
            col_revenue = df_sva.columns[5]
            col_bulan = df_sva.columns[6]
            col_income = df_sva.columns[19]

            if opsi_analisa == "Revenue Analysis (Pendapatan)":
                st.info(f"📈 **Tren Revenue Bulanan (Sumber: data SVA - Kolom {col_revenue})**")
                # Pilih kolom berdasarkan nama aslinya, lalu bersihkan baris kosong (dropna)
                df_chart = df_sva[[col_bulan, col_revenue]].dropna()
                st.line_chart(df_chart.set_index(col_bulan))
                
                # Metrik nilai terkini (baris terakhir)
                val_rev = df_sva[col_revenue].iloc[-1]
                st.metric(label="Revenue Periode Terakhir", value=str(val_rev))

            elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
                st.success(f"💰 **Tren Net Income Bulanan (Sumber: data SVA - Kolom {col_income})**")
                df_chart = df_sva[[col_bulan, col_income]].dropna()
                st.bar_chart(df_chart.set_index(col_bulan))
                
                # Metrik nilai terkini (baris terakhir)
                val_inc = df_sva[col_income].iloc[-1]
                st.metric(label="Net Income Periode Terakhir", value=str(val_inc))
                
        except IndexError:
            st.error("⚠️ Struktur kolom pada sheet 'data SVA' terdeteksi kurang dari 20 kolom (Kolom T tidak terjangkau).")
            st.info(f"Kolom yang berhasil terbaca di sheet Anda saat ini hanya berjumlah: {len(df_sva.columns)} kolom.")
    else:
        st.info("💡 Grafik finansial akan muncul setelah data 'data SVA' sukses dimuat.")

    st.markdown("---")

    # Menampilkan Tabel Utama 'VARCOST' asli di bagian bawah
    st.subheader("📋 Data Sheet Riil: VARCOST")
    df_varcost = ambil_data_sheet("VARCOST")
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True, hide_index=True)
    else:
        st.warning("Data tabel 'VARCOST' kosong atau sedang memuat. Coba klik tombol **REFRESH DATA** di pojok kanan atas.")

# --- HALAMAN LAINNYA ---
def halaman_data_pm():
    st.title("🛠️ Preventive Maintenance Log (data PM)")
    df_pm = ambil_data_sheet("data PM")
    st.dataframe(df_pm, use_container_width=True, hide_index=True) if not df_pm.empty else st.info("Tab 'data PM' kosong.")

def halaman_data_project():
    st.title("🚀 Network Rollout Progress (data Project)")
    df_project = ambil_data_sheet("data Project")
    st.dataframe(df_project, use_container_width=True, hide_index=True) if not df_project.empty else st.info("Tab 'data Project' kosong.")

def halaman_data_asset():
    st.title("🏢 Asset Management Inventory (data Asset)")
    df_asset = ambil_data_sheet("data Asset")
    st.dataframe(df_asset, use_container_width=True, hide_index=True) if not df_asset.empty else st.info("Tab 'data Asset' kosong.")

def halaman_data_kpi():
    st.title("📈 Network Performance Indicator (data KPI)")
    df_kpi = ambil_data_sheet("data KPI")
    st.dataframe(df_kpi, use_container_width=True, hide_index=True) if not df_kpi.empty else st.info("Tab 'data KPI' kosong.")

def halaman_data_operational():
    st.title("⚙️ Network Operations Data (data Operational)")
    df_ops = ambil_data_sheet("data Operational")
    st.dataframe(df_ops, use_container_width=True, hide_index=True) if not df_ops.empty else st.info("Tab 'data Operational' kosong.")

def halaman_data_pjb():
    st.title("⏳ PJB Aging Log (data PJB aging)")
    df_pjb = ambil_data_sheet("data PJB aging")
    st.dataframe(df_pjb, use_container_width=True, hide_index=True) if not df_pjb.empty else st.info("Tab 'data PJB aging' kosong.")

def halaman_monitoring_mbp():
    st.title("📡 Monitoring MBP & Progress Mateline Management")
    st.info("Struktur penampung siap pakai untuk modul tambahan.")

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
