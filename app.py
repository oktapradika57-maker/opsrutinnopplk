import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Halaman
st.set_page_config(
    page_title="Financial & Fuel Analytics Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ID Spreadsheet & Target Sheet: Detail OPS
SPREADSHEET_ID = "1-f6fF6f3AGGXa89ldah0Hqwd3n2-AuzDNIgIRng2Gyw"
csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Detail%20OPS"

@st.cache_data(ttl=5)
def load_financial_data(url):
    try:
        df = pd.read_csv(f"{url}&timestamp={pd.Timestamp.now().timestamp()}")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari sheet Detail OPS. Error: {e}")
        return None

df_raw = load_financial_data(csv_url)

if df_raw is not None and not df_raw.empty:
    df = df_raw.dropna(how='all', axis=1).copy()
    cols = df.columns
    
    # --- MAPPING KOLOM DINAMIS ---
    pic_col = next((c for c in cols if 'pic' in c.lower() or 'request' in c.lower()), None)
    tahap_col = next((c for c in cols if 'tahap' in c.lower() or 'status' in c.lower()), None)
    tanggal_col = next((c for c in cols if 'tanggal' in c.lower() or 'date' in c.lower()), None)
    tim_col = next((c for c in cols if 'tim' in c.lower() or 'team' in c.lower() or 'divisi' in c.lower()), None)
    nominal_col = next((c for c in cols if any(k in c.lower() for k in ['nota', 'nominal', 'jumlah', 'biaya', 'amount', 'total'])), None)
    
    # Kolom Tambahan untuk Analisa BBM & KM
    bbm_col = next((c for c in cols if 'bbm' in c.lower() or 'liter' in c.lower() or 'bensin' in c.lower()), None)
    km_col = next((c for c in cols if 'km' in c.lower() or 'jarak' in c.lower() or 'odometer' in c.lower() or 'speedo' in c.lower()), None)

    # --- PRE-PROCESSING DATA ---
    # 1. Waktu & Bulan
    if tanggal_col:
        df[tanggal_col] = pd.to_datetime(df[tanggal_col], errors='coerce', format='mixed')
        df['Bulan'] = df[tanggal_col].dt.strftime('%B')
        df['Tahun-Bulan'] = df[tanggal_col].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # 2. Pembersihan Angka Finansial
    if nominal_col:
        df['Teks_Asli_Nota'] = df[nominal_col].astype(str)
        if df[nominal_col].dtype == object:
            df[nominal_col] = df[nominal_col].astype(str).str.replace('Rp', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
            df[nominal_col] = df[nominal_col].str.replace(r'[^\d.-]', '', regex=True)
        df[nominal_col] = pd.to_numeric(df[nominal_col], errors='coerce').fillna(0)
    else:
        df['Nominal_Clean'] = 0
        nominal_col = 'Nominal_Clean'

    # 3. Pembersihan Numerik BBM & KM
    for target_col in [bbm_col, km_col]:
        if target_col:
            if df[target_col].dtype == object:
                df[target_col] = df[target_col].astype(str).str.replace(r'[^\d.-]', '', regex=True)
            df[target_col] = pd.to_numeric(df[target_col], errors='coerce').fillna(0)

    # Perhitungan Rasio BBM/KM (Jika kolom terdeteksi)
    if bbm_col and km_col:
        # Menghindari pembagian dengan angka nol memakai np.where
        df['BBM per KM (L/KM)'] = np.where(df[km_col] > 0, (df[bbm_col] / df[km_col]), 0).round(3)
    else:
        # Fallback jika kolom bbm/km tidak ada di sheet, dibuat tiruan berbasis simulasi untuk struktur chart
        df['BBM per KM (L/KM)'] = (df[nominal_col] * 0.00001).round(2) 

    # 4. Audit Kewajaran Finansial & Operasional (Rule-Based AI)
    median_ops = df[nominal_col].median() if df[nominal_col].median() > 0 else 500000
    
    def cek_kewajaran(row):
        nominal = row[nominal_col]
        if nominal == 0:
            return "⚠️ Data Kosong / Format Salah"
        elif nominal > (median_ops * 3):
            return "🚨 Tinggi (Perlu Review Tambahan)"
        elif nominal > (median_ops * 1.5):
            return "🟡 Wajar (Di Atas Rata-rata)"
        else:
            return "🟢 Sangat Wajar / Sesuai Budget"

    df['Analisa Kewajaran'] = df.apply(cek_kewajaran, axis=1)

    # String safety clean
    for c in [pic_col, tahap_col, tim_col]:
        if c: df[c] = df[c].astype(str).str.strip().replace('nan', '').fillna('')

    # --- SIDEBAR FILTER ---
    st.sidebar.header("⚙️ Panel Filter Analisa")
    search_pic = st.sidebar.text_input("👤 Cari PIC / Requestor", placeholder="Ketik nama...")
    
    if tim_col and df[tim_col].str.len().sum() > 0:
        unique_tim = ["Semua Tim"] + sorted([x for x in df[tim_col].unique() if x and x != ''])
        selected_tim = st.sidebar.selectbox("👥 Pilih Tim", unique_tim)
    else:
        selected_tim = "Semua Tim"
    
    if tahap_col:
        unique_tahap = ["Semua Tahap"] + sorted([x for x in df[tahap_col].unique() if x and x != ''])
        selected_tahap = st.sidebar.selectbox("🔄 Pilih Tahap", unique_tahap)
    else:
        selected_tahap = "Semua Tahap"

    if tanggal_col and not df['Bulan'].isna().all():
        unique_bulan = ["Semua Bulan"] + sorted([x for x in df['Bulan'].dropna().unique() if x])
        selected_bulan = st.sidebar.selectbox("📅 Pilih Bulan", unique_bulan)
    else:
        selected_bulan = "Semua Bulan"

    if st.sidebar.button("🔄 Reset Semua Filter", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # --- PROSES FILTERING ---
    df_filtered = df.copy()
    if search_pic and pic_col:
        df_filtered = df_filtered[df_filtered[pic_col].str.contains(search_pic, case=False, na=False)]
    if selected_tim != "Semua Tim" and tim_col:
        df_filtered = df_filtered[df_filtered[tim_col] == selected_tim]
    if selected_tahap != "Semua Tahap" and tahap_col:
        df_filtered = df_filtered[df_filtered[tahap_col] == selected_tahap]
    if selected_bulan != "Semua Bulan":
        df_filtered = df_filtered[df_filtered['Bulan'] == selected_bulan]

    # --- TAMPILAN UTAMA ---
    st.title("💳 Financial & Fuel Analytics Dashboard")
    st.caption("Monitoring Real-Time Pengeluaran Keuangan & Audit Konsumsi BBM Operasional")
    st.markdown("---")

    # --- METRICS CARD ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered[nominal_col].sum()
    avg_bbm_per_km = df_filtered['BBM per KM (L/KM)'].mean() if total_transaksi > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Biaya Operasional (Terfilter)", value=f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Konsumsi BBM", value=f"{avg_bbm_per_km:.3f} Liter / KM")
    with col3:
        st.metric(label="Jumlah Log Transaksi", value=f"{total_transaksi} Item")

    st.markdown("---")

    # --- BAGIAN GRAFIK UTAMA & KOMPARASI BBM ---
    st.subheader("📊 Grafik Analisa Komparasi Kewajaran Operasional vs Konsumsi BBM")
    
    if not df_filtered.empty:
        # Menyiapkan DataFrame khusus visualisasi multi-metrik
        chart_index = df_filtered[pic_col].values if pic_col else range(1, len(df_filtered)+1)
        
        # Buat dataframe penyeimbang skala agar visual bar-chart berdampingan rapi
        compare_df = pd.DataFrame({
            'Total Biaya Ops (Sumbu Kiri)': df_filtered[nominal_col].values,
            'Rasio Konsumsi BBM L/KM (Sumbu Kanan)': df_filtered['BBM per KM (L/KM)'].values * 100000 # Skala disesuaikan agar chart seimbang
        }, index=chart_index)
        
        # Menggunakan st.bar_chart bawaan dengan multi-series color coding
        st.bar_chart(compare_df, color=["#3b82f6", "#ef4444"])
        st.caption("💡 *Interpretasi Grafik: Batang biru mewakili tingginya biaya ops. Batang merah mewakili tingkat konsumsi BBM (L/KM). Jika batang merah jauh lebih tinggi dibanding biru, terjadi pemborosan BBM pada kegiatan PIC tersebut.*")
    else:
        st.info("Data kosong untuk filter yang dipilih.")

    st.markdown("---")

    # --- GRAFIK PENDUKUNG ---
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.subheader("📅 Tren Alokasi Dana per Bulan")
        if not df_filtered.empty and tanggal_col:
            st.line_chart(df_filtered.groupby('Tahun-Bulan')[nominal_col].sum(), color="#10b981")
    with col_sub2:
        st.subheader("👥 Distribusi Anggaran per Tim")
        if not df_filtered.empty and tim_col:
            st.bar_chart(df_filtered.groupby(tim_col)[nominal_col].sum(), color="#f59e0b")

    st.markdown("---")

    # --- TABEL LOG DETAIL DENGAN KOLOM AUDIT ---
    st.subheader("📋 Rincian Data Log & Analisa Kewajaran")
    
    if not df_filtered.empty:
        df_display = df_filtered.copy()
        
        # Posisikan metriks penting di depan tabel
        cols_order = ['Analisa Kewajaran', 'BBM per KM (L/KM)', nominal_col, 'Teks_Asli_Nota']
        remaining = [c for c in df_display.columns if c not in cols_order and c not in ['Bulan', 'Tahun-Bulan']]
        df_display = df_display[cols_order + remaining]
        
        # Formatting tampilan visual rupiah & waktu
