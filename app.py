import streamlit as st
import pandas as pd
import numpy as np

# 1. KONFIGURASI HALAMAN MALAHAN UTAMA
st.set_page_config(
    page_title="Financial Operations Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ID Spreadsheet & Target Sheet: Detail OPS
SPREADSHEET_ID = "1-f6fF6f3AGGXa89ldah0Hqwd3n2-AuzDNIgIRng2Gyw"
# Menggunakan gviz/tq kembali tanpa cache timestamp yang memicu Error 400, terbukti ampuh memaksa data struktural terbaca
csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Detail%20OPS"

st.title("💳 Financial Operations Dashboard")
st.caption("Analisa Real-Time Pengeluaran & Anggaran Operasional Finansial (Sheet: Detail OPS)")
st.markdown("---")

# 2. FUNGSI PEMUAT DATA DENGAN PREVENTING TIMEOUT
@st.cache_data(ttl=5)
def load_financial_data(url):
    try:
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
    # 4. MEMBERSIHKAN KOLOM UNNAMED AKIBAT BARIS KOSONG DI SPREADSHEET
    # Menghapus kolom yang seluruh barisnya kosong sekaligus mengabaikan baris rusak di atas
    df = df_raw.dropna(how='all', axis=1).copy()
    df = df.dropna(how='all', axis=0)

    # =========================================================================
    # ⚠️ KUNCI NAMA KOLOM MANUAL SESUAI DI GOOGLE SHEETS ANDA
    # =========================================================================
    KOLOM_TEXT_NOTA_ASLI = "Total Biaya Sesuai Nota" 
    PIC_KOLOM_ASLI       = "PIC"                      
    TIM_KOLOM_ASLI       = "Tim"                      
    TAHAP_KOLOM_ASLI     = "Tahap"                    
    TANGGAL_KOLOM_ASLI   = "Tanggal"                  
    # =========================================================================

    # Validasi dan penanganan darurat dinamis jika kolom masih tidak terbaca akibat spasi di spreadsheet
    if KOLOM_TEXT_NOTA_ASLI not in df.columns:
        # Cari nama kolom terdekat yang mengandung kata 'Nota' atau 'Biaya' jika terjadi salah ketik di spreadsheet
        kolom_mirip = [c for c in df.columns if 'Nota' in str(c) or 'Biaya' in str(c)]
        if kolom_mirip:
            KOLOM_TEXT_NOTA_ASLI = kolom_mirip[0]
        else:
            st.error(f"❌ Kolom bernama '{KOLOM_TEXT_NOTA_ASLI}' tidak ditemukan.")
            st.info(f"Kolom yang terdeteksi saat ini adalah: {list(df.columns)}")
            st.markdown("💡 *Pastikan baris pertama di Google Sheets Anda langsung berisi Judul Kolom (Header).*")
            st.stop()

    # --- PROSES PEMBERSIHAN DATA ---
    df['Teks_Mentah_Nota'] = df[KOLOM_TEXT_NOTA_ASLI].astype(str).str.strip()
    
    # Bersihkan teks nota asli menjadi angka murni
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].astype(str).str.replace('Rp', '', regex=False)
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace('.', '', regex=False)
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace(',', '.', regex=False)
    df[KOLOM_TEXT_NOTA_ASLI] = df[KOLOM_TEXT_NOTA_ASLI].str.replace(r'[^\d.-]', '', regex=True)
    df[KOLOM_TEXT_NOTA_ASLI] = pd.to_numeric(df[KOLOM_TEXT_NOTA_ASLI], errors='coerce').fillna(0)

    # Penanganan format tanggal secara aman (Menggunakan pd.to_datetime dengan saringan parsial objek)
    if TANGGAL_KOLOM_ASLI in df.columns:
        df[TANGGAL_KOLOM_ASLI] = pd.to_datetime(df[TANGGAL_KOLOM_ASLI], errors='coerce')
        # Buat kolom Bulan aman tanpa mengandalkan properti string murni .dt jika ada baris kosong
        df['Bulan'] = df[TANGGAL_KOLOM_ASLI].apply(lambda x: x.strftime('%B') if pd.notnull(x) else "Tidak Ada Data")
        df['Tahun-Bulan'] = df[TANGGAL_KOLOM_ASLI].apply(lambda x: x.strftime('%Y-%m') if pd.notnull(x) else "Tidak Ada Data")
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # Perhitungan Kewajaran Berdasarkan Nilai Tengah (Median)
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

    # Pembersihan string filter kolom
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

    unique_bulan = ["Semua Bulan"] + sorted([x for x in df['Bulan'].unique() if x])
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
            trend_data = df_filtered[df_filtered['Tahun-Bulan'] != "Tidak Ada Data"].groupby('Tahun-Bulan')[KOLOM_TEXT_NOTA_ASLI].sum()
            if not trend_data.empty:
                st.line_chart(trend_data, color="#10b981")
            else:
                st.info("💡 Data tanggal tidak valid untuk membuat grafik tren.")
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
            # Gunakan penanganan lambda string format manual agar terhindar dari NaT error visualizer
            df_display[TANGGAL_KOLOM_ASLI] = df_display[TANGGAL_KOLOM_ASLI].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else "")

        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Tidak ada data log yang cocok dengan filter saat ini.")
