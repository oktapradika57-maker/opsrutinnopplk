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

# 🌐 FUNGSI UTAMA: Jalur Ekspor CSV Standar Google (Paling Stabil)
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
        st.grid = None
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

    df_sva_raw = ambil_data_sheet("data SVA")

    if not df_sva_raw.empty:
        try:
            df_sva = df_sva_raw.copy()
            df_sva.columns = df_sva.columns.str.strip().str.lower()

            col_bulan = next((c for c in df_sva.columns if "bulan" in c), None)
            col_revenue = next((c for c in df_sva.columns if "revenue" in c), None)
            col_income = next((c for c in df_sva.columns if "income" in c or "laba" in c), None)

            if col_bulan and col_revenue and col_income:
                df_sva[col_revenue] = df_sva[col_revenue].astype(str).str.replace(r'[^\d,-]', '', regex=True).str.replace(',', '.')
                df_sva[col_revenue] = pd.to_numeric(df_sva[col_revenue], errors='coerce').fillna(0)

                df_sva[col_income] = df_sva[col_income].astype(str).str.replace(r'[^\d,-]', '', regex=True).str.replace(',', '.')
                df_sva[col_income] = pd.to_numeric(df_sva[col_income], errors='coerce').fillna(0)

                if opsi_analisa == "Revenue Analysis (Pendapatan)":
                    st.info(f"📈 **Tren Revenue Bulanan (Sumber otomatis terdeteksi: '{col_revenue}')**")
                    df_chart = df_sva[[col_bulan, col_revenue]].dropna()
                    df_chart = df_chart[df_chart[col_bulan].astype(str).str.lower() != "nan"]
                    st.line_chart(df_chart.set_index(col_bulan))
                    
                    total_akumulasi_revenue = df_sva[col_revenue].sum()
                    
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric(label="💰 TOTAL SELURUH REVENUE", value=f"{total_akumulasi_revenue:,.0f}".replace(",", "."))
                    with m2:
                        val_rev_terakhir = df_sva[col_revenue].iloc[-1]
                        st.metric(label="📅 Revenue Periode Terakhir", value=f"{val_rev_terakhir:,.0f}".replace(",", "."))

                elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
                    st.success(f"💰 **Tren Net Income Bulanan (Sumber otomatis terdeteksi: '{col_income}')**")
                    df_chart = df_sva[[col_bulan, col_income]].dropna()
                    df_chart = df_chart[df_chart[col_bulan].astype(str).str.lower() != "nan"]
                    st.bar_chart(df_chart.set_index(col_bulan))
                    
                    total_akumulasi_income = df_sva[col_income].sum()
                    
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric(label="💵 TOTAL SELURUH NET INCOME", value=f"{total_akumulasi_income:,.0f}".replace(",", "."))
                    with m2:
                        val_inc_terakhir = df_sva[col_income].iloc[-1]
                        st.metric(label="📅 Net Income Periode Terakhir", value=f"{val_inc_terakhir:,.0f}".replace(",", "."))
            else:
                st.warning("⚠️ Kolom finansial tidak lengkap di sheet 'data SVA'.")
                st.info(f"Kolom terbaca: {list(df_sva_raw.columns)}")
                
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

# --- FUNGSI HALAMAN LIVE DENGAN FORMULA RAPI ---
def tampilkan_halaman_standar(judul_page, nama_tab_sheet):
    st.title(judul_page)
    df_data = ambil_data_sheet(nama_tab_sheet)
    if not df_data.empty:
        st.dataframe(df_data, use_container_width=True, hide_index=True)
    else:
        st.info(f"Tab '{nama_tab_sheet}' kosong atau sedang menyinkronkan data.")

# ==========================================
# 4. DICTIONARY MAPPING ROUTER (ANTI-CRASH)
# ==========================================
peta_halaman = {
    "VARCOST": halaman_varcost,
    "DATA_PM": lambda: tampilkan_halaman_standar("🛠️ Preventive Maintenance Log (data PM)", "data PM"),
    "DATA_PROJECT": lambda: tampilkan_halaman_standar("🚀 Network Rollout Progress (data Project)", "data Project"),
    "DATA_ASSET": lambda: tampilkan_halaman_standar("🏢 Asset Management Inventory (data Asset)", "data Asset"),
    "DATA_KPI": lambda: tampilkan_halaman_standar("📈 Network Performance Indicator (data KPI)", "data KPI"),
    "DATA_OPERATIONAL": lambda: tampilkan_halaman_standar("⚙️ Network Operations Data (data Operational)", "data Operational"),
    "DATA_PJB": lambda: tampilkan_halaman_standar("⏳ PJB Aging Log (data PJB aging)", "data PJB aging"),
    "MONITORING_MBP": lambda: st.info("📡 Wadah monitoring tambahan siap pakai.")
}

# Eksekusi aman tanpa percabangan if/elif menggantung
if st.session_state.active_menu in peta_halaman:
    peta_halaman[st.session_state.active_menu]()
