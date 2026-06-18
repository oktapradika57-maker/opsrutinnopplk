import streamlit as st
import pandas as pd
import numpy as np
import urllib.request

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Financial Operations Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ID Spreadsheet & Target Sheet: Detail OPS
SPREADSHEET_ID = "1-f6fF6f3AGGXa89ldah0Hqwd3n2-AuzDNIgIRng2Gyw"
csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Detail%20OPS"

st.title("💳 Financial Operations Dashboard")
st.caption("Monitoring Real-Time Alokasi Pengeluaran Finansial & Audit Kewajaran Budget Operasional")
st.markdown("---")

# 2. FUNGSI PEMUAT DATA AMAN (MENGGUNAKAN URLLIB UNTUK TIMEOUT NYATA)
@st.cache_data(ttl=5)
def load_financial_data(url):
    try:
        # Menghindari crash pandas dengan mengatur timeout menggunakan urllib bawaan python
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            df = pd.read_csv(response)
        return df
    except Exception as e:
        return str(e)

# Tampilkan indikator loading
with st.spinner("🔄 Sedang mengunduh data terbaru dari Google Sheets..."):
    df_raw = load_financial_data(csv_url)

# 3. PENANGANAN JIKA KONEKSI GAGAL
if isinstance(df_raw, str):
    st.error("⚠️ Gagal memuat data dari Google Sheets.")
    st.markdown(f"""
    **Detail Masalah:** `{df_raw}`
    
    ### 🛠️ Langkah Solusi Cepat:
    1. **Pastikan Akses Google Sheets:** Klik tombol **Share (Bagikan)** di kanan atas Google Sheets Anda, ubah akses umum menjadi **"Anyone with the link can view"** (Siapa saja yang memiliki link dapat melihat).
    2. **Periksa Nama Tab:** Pastikan nama tab paling bawah di Google Sheets Anda ditulis persis **`Detail OPS`** (perhatikan huruf besar/kecil dan spasinya).
    """)
    if st.button("🔄 Coba Sambungkan Kembali", type="primary"):
        st.cache_data.clear()
        st.rerun()
    st.stop()

elif df_raw is None or df_raw.empty:
    st.warning("⚠️ Koneksi berhasil, namun data di dalam sheet 'Detail OPS' kosong.")
    st.stop()

else:
    # 4. EKSEKUSI JIKA DATA BERHASIL DIUNDUH
    df = df_raw.dropna(how='all', axis=1).copy()
    
    # =========================================================================
    # ⚠️ KUNCI NAMA KOLOM MANUAL SESUAI DI GOOGLE SHEETS ANDA
    # =========================================================================
    KOLOM_TEXT_NOTA_ASLI = "Total Biaya Sesuai Nota" # Kolom teks berisi Rp yang akan dihitung ke grafik
    PIC_KOLOM_ASLI       = "PIC"                      
    TIM_KOLOM_ASLI       = "Tim"                      
    TAHAP_KOLOM_ASLI     = "Tahap"                    
    TANGGAL_KOLOM_ASLI   = "Tanggal"                  
    # =========================================================================

    # Validasi apakah kolom nominal ada
    if KOLOM_TEXT_NOTA_ASLI not in df.columns:
        st.error(f"❌ Kolom bernama '{KOLOM_TEXT_NOTA_ASLI}' tidak ditemukan.")
        st.info(f"Kolom yang terdeteksi saat ini adalah: {list(df.columns)}")
        st.markdown("💡 *Silakan sesuaikan tulisan di baris kode nomor 62 dengan nama kolom yang benar.*")
        st.stop()

    # --- PROSES PEMBERSIHAN DATA ---
    # Simpan teks asli untuk ditampilkan berdampingan di tabel bawah
    df['Teks_Mentah_Nota'] = df[KOLOM_TEXT_NOTA_ASLI].astype(str).str.strip()
    
    # Bersihkan string agar dikonversi murni menjadi angka untuk hitungan grafik & nominal total
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].astype(str).str.replace('Rp', '', regex=False)
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace('.', '', regex=False)
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace(',', '.', regex=False)
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace(r'[^\d.-]', '', regex=True)
    df[KOLOM_TEXT_NOTA_ASLI] = pd.to_numeric(df[KOLOM_TEXT_NOTA_ASLI], errors='coerce').fillna(0)

    # Penanganan format tanggal
    if TANGGAL_KOLOM_ASLI in df.columns:
        df[TANGGAL_KOLOM_ASLI] = pd.to_datetime(df[TANGGAL_KOLOM_ASLI], errors='coerce')
        df[TANGGAL_KOLOM_ASLI] = df[TANGGAL_KOLOM_ASLI].fillna(pd.Timestamp.now())
        df['Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%B')
        df['Tahun-Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # Perhitungan Kewajaran Berdasarkan Nilai Tengah (Median) Angka Hasil Bersih Teks Nota
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
            return "🟢 Sangat Wajar"

    df['Analisa Kewajaran'] = df.apply(cek_kewajaran, axis=1)

    # Hilangkan nan tipe campuran pada filter sidebar
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

    if st.sidebar.button("🔄 Reset & Refresh Dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # --- PROSES PENYARINGAN FILTER ---
    df_filtered = df.copy()
    if search_pic and PIC_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[PIC_KOLOM_ASLI].str.contains(search_pic, case=False, na=False)]
    if selected_tim != "Semua Tim" and TIM_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TIM_KOLOM_ASLI] == selected_tim]
    if selected_tahap != "Semua Tahap" and TAHAP_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TAHAP_KOLOM_ASLI] == selected_tahap]
    if selected_bulan != "Semua Bulan":
        df_filtered = df_filtered[df_filtered['Bulan'] == selected_bulan]

    # --- CARD KPI METRIKS DI UTAMA (TOTAL DI AWAL) ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered[KOLOM_TEXT_NOTA_ASLI].sum()
    rata_rata_biaya = df_filtered[KOLOM_TEXT_NOTA_ASLI].mean() if total_transaksi > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Dana Operasional Terfilter", value=f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Biaya", value=f"Rp {rata_rata_biaya:,.0f}".replace(",", "."))
    with col3:
        st.metric(label="Jumlah Baris Log Terhitung", value=f"{total_transaksi} Item")

    st.markdown("---")

    # --- GRAFIK NOMINAL ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📅 Tren Total Pengeluaran Berdasarkan Bulan")
        if not df_filtered.empty and total_pengeluaran > 0:
            trend_data = df_filtered.groupby('Tahun-Bulan')[KOLOM_TEXT_NOTA_ASLI].sum()
            st.line_chart(trend_data, color="#10b981
