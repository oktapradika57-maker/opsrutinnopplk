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

# Memuat Data Otomatis (Menggunakan TTL 5 detik agar data selalu auto-update dari Google Sheets)
@st.cache_data(ttl=5)
def load_financial_data(url):
    try:
        # Menambahkan parameter acak kecil agar Google tidak menyajikan cache lama browser
        df = pd.read_csv(f"{url}&timestamp={pd.Timestamp.now().timestamp()}")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari sheet Detail OPS. Pastikan link sudah 'Anyone with link can view'. Error: {e}")
        return None

df_raw = load_financial_data(csv_url)

if df_raw is not None and not df_raw.empty:
    # Bersihkan kolom kosong akibat pembacaan otomatis gviz
    df = df_raw.dropna(how='all', axis=1).copy()
    cols = df.columns
    
    # --- MAPPING KOLOM SECARA DINAMIS ---
    pic_col = next((c for c in cols if 'pic' in c.lower() or 'request' in c.lower()), None)
    tahap_col = next((c for c in cols if 'tahap' in c.lower() or 'status' in c.lower()), None)
    tanggal_col = next((c for c in cols if 'tanggal' in c.lower() or 'date' in c.lower()), None)
    nominal_col = next((c for c in cols if any(k in c.lower() for k in ['nominal', 'jumlah', 'biaya', 'amount', 'total', 'debit', 'kredit'])), None)

    # --- PRE-PROCESSING DATA ---
    # 1. Standarisasi Tanggal & Ekstrak Bulan
    if tanggal_col:
        df[tanggal_col] = pd.to_datetime(df[tanggal_col], errors='coerce', format='mixed')
        df['Bulan'] = df[tanggal_col].dt.strftime('%B')
        df['Tahun-Bulan'] = df[tanggal_col].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # 2. Standarisasi Nominal Angka Keuangan
    if nominal_col:
        if df[nominal_col].dtype == object:
            df[nominal_col] = df[nominal_col].astype(str).str.replace(r'[^\d.-]', '', regex=True)
        df[nominal_col] = pd.to_numeric(df[nominal_col], errors='coerce').fillna(0)
    else:
        df['Nominal_Clean'] = 0
        nominal_col = 'Nominal_Clean'

    # Pastikan data string filter aman
    for c in [pic_col, tahap_col]:
        if c: df[c] = df[c].astype(str).replace('nan', '').fillna('')

    # --- SIDEBAR FILTER (MINIMALIS) ---
    st.sidebar.header("⚙️ Filter Analisa")
    
    # Filter 1: Pencarian Teks PIC / Requestor
    search_pic = st.sidebar.text_input("👤 Cari PIC / Requestor", placeholder="Ketik nama...")
    
    # Filter 2: Dropdown Tahap
    if tahap_col:
        unique_tahap = ["Semua Tahap"] + sorted([x for x in df[tahap_col].unique().tolist() if x])
        selected_tahap = st.sidebar.selectbox("🔄 Pilih Tahap", unique_tahap)
    else:
        selected_tahap = "Semua Tahap"

    # Filter 3: Dropdown Bulan
    if tanggal_col and not df['Bulan'].isna().all():
        unique_bulan = ["Semua Bulan"] + sorted([x for x in df['Bulan'].dropna().unique().tolist() if x])
        selected_bulan = st.sidebar.selectbox("📅 Pilih Bulan", unique_bulan)
    else:
        selected_bulan = "Semua Bulan"

    # Tombol Force Refresh Data Manual jika dibutuhkan cepat
    if st.sidebar.button("🔄 Paksa Refresh Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # --- PROSES FILTERING DATA ---
    df_filtered = df.copy()
    if search_pic and pic_col:
        df_filtered = df_filtered[df_filtered[pic_col].str.contains(search_pic, case=False, na=False)]
    if selected_tahap != "Semua Tahap" and tahap_col:
        df_filtered = df_filtered[df_filtered[tahap_col] == selected_tahap]
    if selected_bulan != "Semua Bulan":
        df_filtered = df_filtered[df_filtered['Bulan'] == selected_bulan]

    # --- TAMPILAN UTAMA DASHBOARD ---
    st.title("💳 Financial Operations Dashboard")
    st.caption("Analisa Real-Time Pengeluaran & Anggaran Operasional Finansial (Sheet: Detail OPS)")
    st.info("🔄 Dashboard ini otomatis memperbarui data secara langsung jika Google Sheets diupdate (Auto-refresh 5s).")
    st.markdown("---")

    # --- CARD KPI UTAMA ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered[nominal_col].sum()
    rata_rata_biaya = df_filtered[nominal_col].mean() if total_transaksi > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        # FIX: Menggunakan variabel total_pengeluaran yang benar untuk menghindari NameError
        st.metric(label="Total Dana Operasional Terfilter", value=f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Per Transaksi", value=f"Rp {rata_rata_biaya:,.0f}".replace(",", "."))
    with col3:
        st.metric(label="Volume Kegiatan / Request", value=f"{total_transaksi} Kali")

    st.markdown("---")

    # --- BAGIAN GRAFIK ANALISA ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📊 Tren Pengeluaran Akumulatif per Waktu")
        if not df_filtered.empty and tanggal_col:
            trend_data = df_filtered.groupby('Tahun-Bulan')[nominal_col].sum()
            st.line_chart(trend_data, color="#10b981") 
        else:
            st.info("Data tidak cukup untuk menampilkan tren waktu.")

    with col_chart2:
        st.subheader("📈 Total Pengeluaran Berdasarkan PIC / Requestor")
        if not df_filtered.empty and pic_col:
            # Mengelompokkan total nominal biaya berdasarkan masing-masing PIC
            pic_chart_data = df_filtered.groupby(pic_col)[nominal_col].sum().sort_values(ascending=False).head(10)
            st.bar_chart(pic_chart_data, color="#3b82f6") 
        else:
            st.info("Data tidak cukup untuk menampilkan grafik pengeluaran PIC.")

    st.markdown("---")

    # --- TABEL LOG DETAIL OPERASIONAL ---
    st.subheader("📋 Rincian Data Log Keuangan Operasional")
    
    if not df_filtered.empty:
        df_display = df_filtered.copy()
        if nominal_col in df_display.columns:
            df_display[nominal_col] = df_display[nominal_col].map("Rp {:,.0f}".format)
        
        if tanggal_col in df_display.columns:
            df_display[tanggal_col] = df_display[tanggal_col].dt.strftime('%Y-%m-%d').fillna('-')

        df_display = df_display.drop(columns=['Bulan', 'Tahun-Bulan'], errors='ignore')
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Data keuangan tidak ditemukan untuk kombinasi filter ini.")
else:
    st.info("Memproses atau mendownload data operasional dari tautan spreadsheet Anda...")
