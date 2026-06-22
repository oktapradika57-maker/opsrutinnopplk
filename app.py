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

# ID Spreadsheet Utama Anda (Database Reg Kalimantan)
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

# 🌐 FUNGSI UTAMA: Jalur Ekspor CSV Langsung yang Terbukti Paling Kuat Menembus Google Sheets
@st.cache_data(ttl=2)
def ambil_data_sheet(nama_sheet):
    try:
        sheet_aman = urllib.parse.quote(nama_sheet)
        url_csv = f"https://google.com{SPREADSHEET_ID}/export?format=csv&sheet={sheet_aman}"
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
        st.session_state.active_menu = "VARCOST"
        st.session_state.play_sound = True
        st.rerun()
with col2:
    if st.button("🛠️\n\nDATA PM", use_container_width=True, key="btn_pm"):
        st.session_state.active_menu = "DATA_PM"
        st.session_state.play_sound = True
        st.rerun()
with col3:
    if st.button("🚀\n\nDATA PROJECT", use_container_width=True, key="btn_project"):
        st.session_state.active_menu = "DATA_PROJECT"
        st.session_state.play_sound = True
        st.rerun()
with col4:
    if st.button("🏢\n\nDATA ASSET", use_container_width=True, key="btn_asset"):
        st.session_state.active_menu = "DATA_ASSET"
        st.session_state.play_sound = True
        st.rerun()
with col5:
    if st.button("📈\n\nDATA KPI", use_container_width=True, key="btn_kpi"):
        st.session_state.active_menu = "DATA_KPI"
        st.session_state.play_sound = True
        st.rerun()
with col6:
    if st.button("⚙️\n\nDATA OPERATIONAL", use_container_width=True, key="btn_operational"):
        st.session_state.active_menu = "DATA_OPERATIONAL"
        st.session_state.play_sound = True
        st.rerun()
with col7:
    if st.button("⏳\n\nDATA PJB AGING", use_container_width=True, key="btn_pjb"):
        st.session_state.active_menu = "DATA_PJB"
        st.session_state.play_sound = True
        st.rerun()
with col8:
    if st.button("📡\n\nMONITORING MBP", use_container_width=True, key="btn_mbp"):
        st.session_state.active_menu = "MONITORING_MBP"
        st.session_state.play_sound = True
        st.rerun()
with col_ref:
    if st.button("🔄\n\nREFRESH DATA", use_container_width=True, key="btn_refresh_all", type="primary"):
        st.cache_data.clear()
        st.session_state.play_sound = True
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

    df_sva = ambil_data_sheet("data SVA")

    if not df_sva.empty:
        try:
            col_revenue = df_sva.columns[5]   # Fisik Kolom F
            col_bulan = df_sva.columns[6]     # Fisik Kolom G
            col_income = df_sva.columns[19]   # Fisik Kolom T

            df_sva[col_bulan] = df_sva[col_bulan].astype(str).str.strip()

            df_sva[col_revenue] = df_sva[col_revenue].astype(str).str.replace(r'[^\d,-]', '', regex=True).str.replace(',', '.')
            df_sva[col_revenue] = pd.to_numeric(df_sva[col_revenue], errors='coerce').fillna(0)

            df_sva[col_income] = df_sva[col_income].astype(str).str.replace(r'[^\d,-]', '', regex=True).str.replace(',', '.')
            df_sva[col_income] = pd.to_numeric(df_sva[col_income], errors='coerce').fillna(0)

            if opsi_analisa == "Revenue Analysis (Pendapatan)":
                st.info(f"📈 **Tren Revenue Bulanan (Sumber: data SVA - Kolom {col_revenue})**")
                df_chart = df_sva[[col_bulan, col_revenue]].dropna()
                df_chart = df_chart[df_chart[col_bulan] != "nan"]
                st.line_chart(df_chart.set_index(col_bulan))
                
                total_akumulasi_revenue = df_sva[col_revenue].sum()
                
                m1, m2 = st.columns(2)
                with m1:
                    st.metric(label="💰 TOTAL SELURUH REVENUE", value=f"{total_akumulasi_revenue:,.0f}".replace(",", "."))
                with m2:
                    val_rev_terakhir = df_sva[col_revenue].iloc[-1]
                    st.metric(label="📅 Revenue Periode Terakhir", value=f"{val_rev_terakhir:,.0f}".replace(",", "."))

            elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
                st.success(f"💰 **Tren Net Income Bulanan (Sumber: data SVA - Kolom {col_income})**")
                df_chart = df_sva[[col_bulan, col_income]].dropna()
                df_chart = df_chart[df_chart[col_bulan] != "nan"]
                st.bar_chart(df_chart.set_index(col_bulan))
                
                total_akumulasi_income = df_sva[col_income].sum()
                
                m1, m2 = st.columns(2)
                with m1:
                    st.metric(label="💵 TOTAL SELURUH NET INCOME", value=f"{total_akumulasi_income:,.0f}".replace(",", "."))
                with m2:
                    val_inc_terakhir = df_sva[col_income].iloc[-1]
                    st.metric(label="📅 Net Income Periode Terakhir", value=f"{val_inc_terakhir:,.0f}".replace(",", "."))
                
        except Exception as err:
            st.error(f"Gagal memproses perhitungan angka pada tab 'data SVA': {err}")
    else:
        st.info("💡 Grafik dan perhitungan finansial akan muncul setelah data 'data SVA' berhasil ditarik.")

    st.markdown("---")

    st.subheader("📋 Data Sheet Riil: VARCOST")
    df_varcost = ambil_data_sheet("VARCOST")
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True, hide_index=True)
    else:
        st.warning("Data tabel 'VARCOST' kosong atau sedang memuat. Klik tombol **REFRESH DATA** di pojok kanan atas.")

def halaman_data_pm():
    st.title("🛠️ Preventive Maintenance Log (data PM)")
    df_pm = ambil_data_sheet("data PM")
    if not df_pm.empty:
        st.dataframe(df_pm, use_container_width=True, hide_index=True)
    else:
        st.info("Tab 'data PM' kosong.")

def halaman_data_project():
    st.title("🚀 Network Rollout Progress (data Project)")
    df_project = ambil_data_sheet("data Project")
    if not df_project.empty:
        st.dataframe(df_project, use_container_width=True, hide_index=True)
    else:
        st.info("Tab 'data Project' Team Kosong.")

def halaman_data_asset():
    st.title("🏢 Asset Management Inventory (data Asset)")
    df_asset = ambil_data_sheet("data Asset")
    if not df_asset.empty:
        st.dataframe(df_asset, use_container_width=True, hide_index=True)
    else:
        st.info("Tab 'data Asset' kosong.")

def halaman_data_kpi():
    st.title("📈 Network Performance Indicator (data KPI)")
    df_kpi = ambil_data_sheet("data KPI")
    if not df_kpi.empty:
        st.dataframe(df_kpi, use_container_width=True, hide_index=True)
    else:
        st.info("Tab 'data KPI' kosong.")

def halaman_data_operational():
    st.title("⚙️ Network Operations Data (data Operational)")
    df_ops = ambil_data_sheet("data Operational")
    if not df_ops.empty:
        st.dataframe(df_ops, use_container_width=True, hide_index=True)
    else:
        st.info("Tab 'data Operational' kosong.")

def halaman_data_pjb():
    st.title("⏳ PJB Aging Log (data PJB aging)")
    df_pjb = ambil_data_sheet("data PJB aging")
    if not df_pjb.empty:
        st.dataframe(df_pjb, use_container_width=True, hide_index=True)
    else:
        st.info("Tab 'data PJB aging' kosong.")

def halaman_monitoring_mbp():
    st.title("📡 Monitoring MBP & Progress Mateline Management")
    st.info("Struktur penampung siap pakai untuk modul tambahan.")

# ==========================================
# 4. DICTIONARY ROUTER (ANTI-ERROR SPASI)
# ==========================================
# Struktur peta fungsi halaman untuk menjamin kepresisian eksekusi
peta_halaman = {
    "VARCOST": halaman_varcost,
    "DATA_PM": halaman_data_pm,
    "DATA_PROJECT": halaman_data_project,
    "DATA_ASSET": halaman_data_asset,
    "DATA_KPI": halaman_data_kpi,
    "DATA_OPERATIONAL": halaman_data_operational,
    "DATA_PJB": halaman_data_pjb,
    "MONITORING_MBP": halaman_monitoring_mbp
}

# Jalankan fungsi halaman berdasarkan menu aktif
if st.session_state.active_menu in peta_halaman:
    peta_halaman[st.session_state.active_menu]()
