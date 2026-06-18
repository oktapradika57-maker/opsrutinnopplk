import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Halaman Minimalis & Wide
st.set_page_config(
    page_title="Financial Operations Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ID Spreadsheet & Target Sheet: Detail OPS
SPREADSHEET_ID = "1-f6fF6f3AGGXa89ldah0Hqwd3n2-AuzDNIgIRng2Gyw"
csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Detail%20OPS"

@st.cache_data(ttl=2) # Auto-update super cepat (2 detik) jika Google Sheets berubah
def load_financial_data(url):
    try:
        df = pd.read_csv(f"{url}&timestamp={pd.Timestamp.now().timestamp()}")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari sheet Detail OPS. Error: {e}")
        return None

df_raw = load_financial_data(csv_url)

if df_raw is not None and not df_raw.empty:
    # Buat salinan data dan bersihkan kolom yang sepenuhnya kosong
    df = df_raw.dropna(how='all', axis=1).copy()
    
    # =========================================================================
    # ⚠️ SESUAIKAN NAMA KOLOM DI BAWAH INI DENGAN HEADER DI GOOGLE SHEETS ANDA
    # =========================================================================
    KOLOM_TEXT_NOTA_ASLI = "Total Biaya (Sesuai Nota)" # <-- Ganti dengan nama kolom teks nota Anda jika berbeda
    PIC_KOLOM_ASLI       = "PIC"                      
    TIM_KOLOM_ASLI       = "Tim"                      
    TAHAP_KOLOM_ASLI     = "Tahap"                    
    TANGGAL_KOLOM_ASLI   = "Tanggal"                  
    # =========================================================================

    # Validasi awal apakah nama kolom teks nota tersebut eksis
    if KOLOM_TEXT_NOTA_ASLI not in df.columns:
        st.error(f"❌ Kolom bernama '{KOLOM_TEXT_NOTA_ASLI}' tidak ditemukan. Daftar kolom di Google Sheets Anda: {list(df.columns)}")
        st.stop()

    # --- PRE-PROCESSING & PEMBERSIHAN DATA SEJAK AWAL ---
    
    # Backup teks asli ke kolom baru untuk referensi visual di tabel bawah
    df['Teks_Mentah_Nota'] = df[KOLOM_TEXT_NOTA_ASLI].astype(str).str.strip()
    
    # PROSES KLIPING: Bersihkan teks nota asli agar menjadi ANGKA murni untuk Grafik & Perhitungan Total
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].astype(str).str.replace('Rp', '', regex=False)
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace('.', '', regex=False) # Hilangkan titik ribuan
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace(',', '.', regex=False) # Ubah koma desimal ke titik
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace(r'[^\d.-]', '', regex=True) # Buang sisa text/spasi gaib
    
    # Paksa konversi ke float numerik agar bisa di-SUM dan di-CHART
    df[KOLOM_TEXT_NOTA_ASLI] = pd.to_numeric(df[KOLOM_TEXT_NOTA_ASLI], errors='coerce').fillna(0)

    # 1. Standarisasi Tanggal & Bulan
    if TANGGAL_KOLOM_ASLI in df.columns:
        df[TANGGAL_KOLOM_ASLI] = pd.to_datetime(df[TANGGAL_KOLOM_ASLI], errors='coerce')
        df[TANGGAL_KOLOM_ASLI] = df[TANGGAL_KOLOM_ASLI].fillna(pd.Timestamp.now()) 
        df['Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%B')
        df['Tahun-Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # 2. Hitung Nilai Kewajaran Operasional dari Nominal yang Sudah Bersih
    median_ops = df[KOLOM_TEXT_NOTA_ASLI].median() if df[KOLOM_TEXT_NOTA_ASLI].median() > 0 else 500000
    def cek_kewajaran(row):
        nominal = row[KOLOM_TEXT_NOTA_ASLI]
        if nominal == 0:
            return "⚠️ Format Teks Salah / Kosong"
        elif nominal > (median_ops * 3):
            return "🚨 Tinggi (Perlu Review Tambahan)"
        elif nominal > (median_ops * 1.5):
            return "🟡 Wajar (Di Atas Rata-rata)"
        else:
            return "🟢 Sangat Wajar / Sesuai Budget"

    df['Analisa Kewajaran'] = df.apply(cek_kewajaran, axis=1)

    # Bersihkan string kolom filter dari nilai NaN/kosong campuran
    for c in [PIC_KOLOM_ASLI, TAHAP_KOLOM_ASLI, TIM_KOLOM_ASLI]:
        if c in df.columns: 
            df[c] = df[c].astype(str).str.strip().replace('nan', '').fillna('')

    # --- SIDEBAR PANEL FILTER ---
    st.sidebar.header("⚙️ Panel Filter Analisa")
    search_pic = st.sidebar.text_input("👤 Cari PIC / Requestor", placeholder="Ketik nama...")
    
    if TIM_KOLOM_ASLI in df.columns:
        unique_tim = ["Semua Tim"] + sorted([x for x in df[TIM_KOLOM_ASLI].unique() if x and x != ''])
        selected_tim = st.sidebar.selectbox("👥 Pilih Tim", unique_tim)
    else:
        selected_tim = "Semua Tim"
    
    if TAHAP_KOLOM_ASLI in df.columns:
        unique_tahap = ["Semua Tahap"] + sorted([x for x in df[TAHAP_KOLOM_ASLI].unique() if x and x != ''])
        selected_tahap = st.sidebar.selectbox("🔄 Pilih Tahap", unique_tahap)
    else:
        selected_tahap = "Semua Tahap"

    unique_bulan = ["Semua Bulan"] + sorted([x for x in df['Bulan'].dropna().unique() if x])
    selected_bulan = st.sidebar.selectbox("📅 Pilih Bulan", unique_bulan)

    if st.sidebar.button("🔄 Reset & Refresh Data Manual", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # --- EKSEKUSI PENYARINGAN DATA ---
    df_filtered = df.copy()
    if search_pic and PIC_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[PIC_KOLOM_ASLI].str.contains(search_pic, case=False, na=False)]
    if selected_tim != "Semua Tim" and TIM_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TIM_KOLOM_ASLI] == selected_tim]
    if selected_tahap != "Semua Tahap" and TAHAP_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TAHAP_KOLOM_ASLI] == selected_tahap]
    if selected_bulan != "Semua Bulan":
        df_filtered = df_filtered[df_filtered['Bulan'] == selected_bulan]

    # --- TAMPILAN UTAMA DASHBOARD ---
    st.title("💳 Financial Operations Dashboard")
    st.caption("Monitoring Real-Time Alokasi Pengeluaran Finansial & Audit Kewajaran Budget Operasional")
    st.markdown("---")

    # --- CARD KPI UTAMA (TOTAL DI AWAL) ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered
