import streamlit as st
import pandas as pd
import numpy as np

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Financial Operations Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ID Spreadsheet & Target Sheet: Detail OPS
SPREADSHEET_ID = "1-f6fF6f3AGGXa89ldah0Hqwd3n2-AuzDNIgIRng2Gyw"
# Menggunakan format ekspor CSV resmi Google yang jauh lebih stabil dan anti-Error 400
csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&sheet=Detail%20OPS"

st.title("💳 Financial Operations Dashboard")
st.caption("Analisa Real-Time Pengeluaran & Anggaran Operasional Finansial (Sheet: Detail OPS)")
st.markdown("---")

# 2. FUNGSI PEMUAT DATA AMAN
@st.cache_data(ttl=5)
def load_financial_data(url):
    try:
        # Membaca CSV langsung menggunakan pandas dengan engine default yang stabil
        df = pd.read_csv(url)
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
        st.markdown("💡 *Silakan sesuaikan tulisan di baris kode KOLOM_TEXT_NOTA_ASLI dengan nama kolom yang benar.*")
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

    # Penanganan format tanggal secara aman (Mencegah AttributeError .dt)
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

    # Penanganan konversi string filter secara aman agar tidak crash .fillna
    for c in [PIC_KOLOM_ASLI, TAHAP_KOLOM_ASLI, TIM_KOLOM_ASLI]:
        if c in df.columns:
            df[c] = df[c].fillna('').astype(str).str.strip().replace('nan', '')

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
    total_pengeluaran = df_filtered[KOLOM_TEXT_NOTA_ASLI].sum() # Variabel diperbaiki dari typo 'total_pengraw'
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
            st.line_chart(trend_data, color="#10b981") # Tanda kutip string literal ditutup dengan benar
        else:
            st.info("💡 Grafik tren kosong karena nominal Rp 0 atau filter tidak cocok.")

    with col_chart2:
        st.subheader("👥 Alokasi Pengeluaran per Tim / Divisi")
        if not df_filtered.empty and TIM_KOLOM_ASLI in df_filtered.columns and total_pengeluaran > 0:
            tim_data = df_filtered.groupby(TIM_KOLOM_ASLI)[KOLOM_TEXT_NOTA_ASLI].sum().sort_values(ascending=False)
            st.bar_chart(tim_data, color="#3b82f6")
        else:
            st.info("💡 Grafik alokasi tim kosong karena nominal Rp 0 atau filter tidak cocok.")

    st.markdown("---")

    # --- TABEL DETAIL LOG DATA ---
    st.subheader("📋 Rincian Data Log & Analisa Kewajaran")
    if not df_filtered.empty:
        df_display = df_filtered.copy()
        
        base_cols = ['Analisa Kewajaran', KOLOM_TEXT_NOTA_ASLI, 'Teks_Mentah_Nota']
        remaining_cols = [c for c in df_display.columns if c not in base_cols and c not in ['Bulan', 'Tahun-Bulan']]
        df_display = df_display[base_cols + remaining_cols]
        
        df_display[KOLOM_TEXT_NOTA_ASLI] = df_display[KOLOM_TEXT_NOTA_ASLI].map("Rp {:,.0f}".format)
        if TANGGAL_KOLOM_ASLI in df_display.columns:
            df_display[TANGGAL_KOLOM_ASLI] = df_display[TANGGAL_KOLOM_ASLI].dt.strftime('%Y-%m-%d')

        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Tidak ada data log yang cocok dengan filter saat ini.")
