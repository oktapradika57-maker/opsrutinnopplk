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
# Menggunakan Viz API dengan target sheet name di-encode URL space -> %20
csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Detail%20OPS"

@st.cache_data(ttl=30)
def load_financial_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari sheet Detail OPS. Pastikan link sudah 'Anyone with link can view'. Error: {e}")
        return None

df_raw = load_financial_data(csv_url)

if df_raw is not None and not df_raw.empty:
    # Bersihkan kolom kosong akibat pembacaan otomatis gviz
    df = df_raw.dropna(how='all', axis=1).copy()
    cols = df.columns
    
    # --- MAPPING KOLOM SECARA DINAMIS (Anti-Error Huruf Besar/Kecil) ---
    pic_col = next((c for c in cols if 'pic' in c.lower() or 'request' in c.lower()), None)
    tahap_col = next((c for c in cols if 'tahap' in c.lower() or 'status' in c.lower()), None)
    tanggal_col = next((c for c in cols if 'tanggal' in c.lower() or 'date' in c.lower()), None)
    
    # Cari kolom nominal uang/biaya/amount
    nominal_col = next((c for c in cols if any(k in c.lower() for k in ['nominal', 'jumlah', 'biaya', 'amount', 'total', 'debit', 'kredit'])), None)
    kategori_col = next((c for c in cols if 'kategori' in c.lower() or 'keperluan' in c.lower() or 'keterangan' in c.lower()), cols[0])

    # --- PRE-PROCESSING DATA ---
    # 1. Standarisasi Tanggal & Ekstrak Bulan
    if tanggal_col:
        df[tanggal_col] = pd.to_datetime(df[tanggal_col], errors='coerce', format='mixed')
        # Buat kolom Bulan baru dalam format teks Bahasa Inggris/Angka untuk sorting
        df['Bulan'] = df[tanggal_col].dt.strftime('%B')
        df['Tahun-Bulan'] = df[tanggal_col].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # 2. Standarisasi Nominal Angka Keuangan
    if nominal_col:
        # Bersihkan karakter mata uang (Rp, koma, titik sembarang) jika berupa teks
        if df[nominal_col].dtype == object:
            df[nominal_col] = df[nominal_col].astype(str).str.replace(r'[^\d.-]', '', regex=True)
        df[nominal_col] = pd.to_numeric(df[nominal_col], errors='coerce').fillna(0)
    else:
        df['Nominal_Mok'] = 0
        nominal_col = 'Nominal_Mok'

    # Ensure filter columns are safe strings
    for c in [pic_col, tahap_col]:
        if c: df[c] = df[c].astype(str).fillna('')

    # --- SIDEBAR FILTER (MINIMALIS) ---
    st.sidebar.header("⚙️ Filter Analisa")
    
    # Filter 1: Pencarian Teks PIC / Requestor
    search_pic = st.sidebar.text_input("👤 Cari PIC / Requestor", placeholder="Ketik nama...")
    
    # Filter 2: Dropdown Tahap
    if tahap_col:
        unique_tahap = ["Semua Tahap"] + sorted(df[tahap_col].unique().tolist())
        selected_tahap = st.sidebar.selectbox("🔄 Pilih Tahap", unique_tahap)
    else:
        selected_tahap = "Semua Tahap"

    # Filter 3: Dropdown Bulan
    if tanggal_col and not df['Bulan'].isna().all():
        unique_bulan = ["Semua Bulan"] + sorted(df['Bulan'].dropna().unique().tolist())
        selected_bulan = st.sidebar.selectbox("📅 Pilih Bulan", unique_bulan)
    else:
        selected_bulan = "Semua Bulan"

    if st.sidebar.button("🔄 Reset Semua Filter", use_container_width=True):
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
    st.markdown("---")

    # --- CARD KPI UTAMA ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered[nominal_col].sum()
    rata_rata_biaya = df_filtered[nominal_col].mean() if total_transaksi > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Dana Operasional Terfilter", value=f"Rp {total_pengraw:,.0f}".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Per Transaksi", value=f"Rp {rata_rata_biaya:,.0f}".replace(",", "."))
    with col3:
        st.metric(label="Volume Kegiatan / Request", value=f"{total_transaksi} Kali")

    st.markdown("---")

    # --- BAGIAN GRAFIK ANALISA ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📊 Tren Pengeluaran per Bulan / Waktu")
        if not df_filtered.empty and tanggal_col:
            # Grouping dana berdasarkan waktu tahun-bulan
            trend_data = df_filtered.groupby('Tahun-Bulan')[nominal_col].sum()
            st.line_chart(trend_data, color="#10b981") # Garis Hijau Finansial Emerald
        else:
            st.info("Data tidak cukup untuk menampilkan tren waktu.")

    with col_chart2:
        st.subheader("📈 Distribusi Alokasi Per Tahap")
        if not df_filtered.empty and tahap_col:
            tahap_data = df_filtered.groupby(tahap_col)[nominal_col].sum()
            st.bar_chart(tahap_data, color="#3b82f6") # Bar chart Biru Modern
        else:
            st.info("Data tidak cukup untuk menampilkan distribusi tahap.")

    st.markdown("---")

    # --- TABEL LOG DETAIL OPERASIONAL ---
    st.subheader("📋 Rincian Data Log Keuangan Operasional")
    
    if not df_filtered.empty:
        # Format kolom nominal agar mudah dibaca rupiah di dalam tabel interaktif streamlit
        df_display = df_filtered.copy()
        if nominal_col in df_display.columns:
            df_display[nominal_col] = df_display[nominal_col].map("Rp {:,.0f}".format)
        
        if tanggal_col in df_display.columns:
            df_display[tanggal_col] = df_display[tanggal_col].dt.strftime('%Y-%m-%d').fillna('-')

        # Drop kolom temporary bulan agar tabel asli rapi
        df_display = df_display.drop(columns=['Bulan', 'Tahun-Bulan'], errors='ignore')

        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Data keuangan tidak ditemukan untuk kombinasi filter ini. Silakan periksa atau ubah opsi filter pada sidebar Anda.")
else:
    st.info("Memproses atau mendownload data operasional dari tautan spreadsheet Anda...")
