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

@st.cache_data(ttl=2) # Sinkronisasi data real-time kilat (2 detik) jika Google Sheets diubah
def load_financial_data(url):
    try:
        df = pd.read_csv(f"{url}&timestamp={pd.Timestamp.now().timestamp()}")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari sheet Detail OPS. Error: {e}")
        return None

df_raw = load_financial_data(csv_url)

if df_raw is not None and not df_raw.empty:
    # Buat salinan data dan bersihkan kolom yang kosong
    df = df_raw.dropna(how='all', axis=1).copy()
    
    # =========================================================================
    # ⚠️ KUNCI NAMA KOLOM MANUAL SESUAI DI GOOGLE SHEETS ANDA (BESAR/KECIL HURUF)
    # =========================================================================
    NOMINAL_KOLOM_ASLI = "Total Biaya (Sesuai Nota)"  # <-- Pastikan nama kolom ini sama persis di Sheet Anda
    PIC_KOLOM_ASLI     = "PIC"                      
    TIM_KOLOM_ASLI     = "Tim"                      
    TAHAP_KOLOM_ASLI   = "Tahap"                    
    TANGGAL_KOLOM_ASLI = "Tanggal"                  
    # =========================================================================

    # Validasi awal keberadaan kolom nominal
    if NOMINAL_KOLOM_ASLI not in df.columns:
        st.error(f"❌ Kolom bernama '{NOMINAL_KOLOM_ASLI}' tidak ditemukan. Daftar kolom di Google Sheets Anda saat ini adalah: {list(df.columns)}")
        st.stop()

    # --- PRE-PROCESSING & PEMBERSIHAN DATA ---
    
    # 1. Standarisasi Tanggal & Bulan (Mencegah Error .dt Accessor)
    if TANGGAL_KOLOM_ASLI in df.columns:
        df[TANGGAL_KOLOM_ASLI] = pd.to_datetime(df[TANGGAL_KOLOM_ASLI], errors='coerce')
        df[TANGGAL_KOLOM_ASLI] = df[TANGGAL_KOLOM_ASLI].fillna(pd.Timestamp.now()) # Fallback data kosong
        df['Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%B')
        df['Tahun-Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # 2. Pembersihan Ekstrem Angka Uang/Nominal Finansial
    df['Teks_Asli_Nota'] = df[NOMINAL_KOLOM_ASLI].astype(str).str.strip()
    
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].astype(str).str.replace('Rp', '', regex=False)
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].str.replace('.', '', regex=False) # Hapus titik ribuan Indo
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].str.replace(',', '.', regex=False) # Normalisasi koma desimal
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].str.replace(r'[^\d.-]', '', regex=True) # Hapus teks sisa aneh
    df[NOMINAL_KOLOM_ASLI] = pd.to_numeric(df[NOMINAL_KOLOM_ASLI], errors='coerce').fillna(0)

    # 3. Kolom Analisa Kewajaran Operasional Otomatis Berbasis Median (Uang)
    median_ops = df[NOMINAL_KOLOM_ASLI].median() if df[NOMINAL_KOLOM_ASLI].median() > 0 else 500000
    def cek_kewajaran(row):
        nominal = row[NOMINAL_KOLOM_ASLI]
        if nominal == 0:
            return "⚠️ Format Data Salah / Nol"
        elif nominal > (median_ops * 3):
            return "🚨 Tinggi (Perlu Review Tambahan)"
        elif nominal > (median_ops * 1.5):
            return "🟡 Wajar (Di Atas Rata-rata)"
        else:
            return "🟢 Sangat Wajar / Sesuai Budget"

    df['Analisa Kewajaran'] = df.apply(cek_kewajaran, axis=1)

    # Menghindari error tipe data NaN campuran pada filter dropdown string
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

    # --- EKSEKUSI PENYARINGAN DATA (MULTI-FILTER) ---
    df_filtered = df.copy()
    if search_pic and PIC_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[PIC_KOLOM_ASLI].str.contains(search_pic, case=False, na=False)]
    if selected_tim != "Semua Tim" and TIM_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TIM_KOLOM_ASLI] == selected_tim]
    if selected_tahap != "Semua Tahap" and TAHAP_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TAHAP_KOLOM_ASLI] == selected_tahap]
    if selected_bulan != "Semua Bulan":
        df_filtered = df_filtered[df_filtered['Bulan'] == selected_bulan]

    # --- ELEMEN TAMPILAN DASHBOARD ---
    st.title("💳 Financial Operations Dashboard")
    st.caption("Monitoring Real-Time Alokasi Pengeluaran Finansial & Audit Kewajaran Budget Operasional")
    st.markdown("---")

    # --- CARD KPI UTAMA (METRIKS) ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered[NOMINAL_KOLOM_ASLI].sum()
    rata_rata_biaya = df_filtered[NOMINAL_KOLOM_ASLI].mean() if total_transaksi > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Pengeluaran (Terfilter)", value=f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Biaya", value=f"Rp {rata_rata_biaya:,.0f}".replace(",", "."))
    with col3:
        st.metric(label="Jumlah Transaksi Log", value=f"{total_transaksi} Item")

    st.markdown("---")

    # --- GRAFIK ANALISA NOMINAL FINANSIAL ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📅 Tren Total Pengeluaran Berdasarkan Bulan")
        if not df_filtered.empty and total_pengeluaran > 0:
            trend_data = df_filtered.groupby('Tahun-Bulan')[NOMINAL_KOLOM_ASLI].sum()
            st.line_chart(trend_data, color="#10b981") 
        else:
            st.info("💡 Grafik tren kosong karena nominal Rp 0 atau filter tidak cocok.")

    with col_chart2:
        st.subheader("👥 Alokasi Pengeluaran per Tim / Divisi")
        if not df_filtered.empty and TIM_KOLOM_ASLI in df_filtered.columns and total_pengeluaran > 0:
            tim_data = df_filtered.groupby(TIM_KOLOM_ASLI)[NOMINAL_KOLOM_ASLI].sum().sort_values(ascending=False)
            st.bar_chart(tim_data, color="#3b82f6") 
        else:
            st.info("💡 Grafik divisi kosong karena nama kolom Tim belum sesuai.")

    st.markdown("---")

    # --- TABEL RINCIAN LOG & AUDIT KEWAJARAN ---
    st.subheader("📋 Rincian Data Log & Analisa Kewajaran")
    if not df_filtered.empty:
        df_display = df_filtered.copy()
        
        # Pengaturan Tata Urutan Kolom Utama Tabel
        base_cols = ['Analisa Kewajaran', NOMINAL_KOLOM_ASLI, 'Teks_Asli_Nota']
        remaining_cols = [c for c in df_display.columns if c not in base_cols and c not in ['Bulan', 'Tahun-Bulan']]
        df_display = df_display[base_cols + remaining_cols]
        
        # Format angka desimal tampilan tabel menjadi Rupiah Cantik (.map)
        df_display[NOMINAL_KOLOM_ASLI] = df_display[NOMINAL_KOLOM_ASLI].map("Rp {:,.0f}".format)
        if TANGGAL_KOLOM_ASLI in df_display.columns:
            df_display[TANGGAL_KOLOM_ASLI] = df_display[TANGGAL_KOLOM_ASLI].dt.strftime('%Y-%m-%d')

        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Data log tidak ditemukan untuk kombinasi penyaringan filter ini.")
else:
    st.info("Menyambungkan koneksi log ke Google Sheets...")
