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

@st.cache_data(ttl=2) # TTL sangat kecil agar data langsung terupdate real-time
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
    
    # =========================================================================
    # ⚠️ SILAKAN GANTI TEKS DI BAWAH INI SESUAI NAMA KOLOM ASLI DI GOOGLE SHEETS ANDA
    # =========================================================================
    NOMINAL_KOLOM_ASLI = "Total Biaya (Sesuai Nota)"  # <-- Ganti dengan nama kolom uang Anda
    BBM_KOLOM_ASLI     = "Liter BBM"                # <-- Ganti dengan nama kolom jumlah liter bbm
    KM_KOLOM_ASLI      = "Jenis BBM"                       # <-- Ganti dengan nama kolom Odometer / KM jarak
    PIC_KOLOM_ASLI     = "PIC"                      # <-- Ganti dengan nama kolom nama orang / requestor
    TIM_KOLOM_ASLI     = "Tim"                      # <-- Ganti dengan nama kolom Tim / Divisi
    TAHAP_KOLOM_ASLI   = "Tahap"                    # <-- Ganti dengan nama kolom Tahap / Status
    TANGGAL_KOLOM_ASLI = "Bulan"                  # <-- Ganti dengan nama kolom tanggal kegiatan
    # =========================================================================

    # Pengecekan paksa kolom nominal uang
    if NOMINAL_KOLOM_ASLI not in df.columns:
        st.error(f"❌ Kolom bernama '{NOMINAL_KOLOM_ASLI}' tidak ditemukan di Google Sheets Anda. Kolom yang tersedia saat ini adalah: {list(df.columns)}")
        st.stop()

    # --- PRE-PROCESSING DATA ---
    # 1. Penanganan Waktu & Bulan
    if TANGGAL_KOLOM_ASLI in df.columns:
        df[TANGGAL_KOLOM_ASLI] = pd.to_datetime(df[TANGGAL_KOLOM_ASLI], errors='coerce', format='mixed')
        df['Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%B')
        df['Tahun-Bulan'] = df[TANGGAL_KOLOM_ASLI].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # 2. Pembersihan Angka Finansial Nominal Paksa
    df['Teks_Asli_Nota'] = df[NOMINAL_KOLOM_ASLI].astype(str)
    
    # Hilangkan semua atribut teks finansial Indo / spasi tak terlihat
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].astype(str).str.replace('Rp', '', regex=False)
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].str.replace('.', '', regex=False)
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].str.replace(',', '.', regex=False)
    df[NOMINAL_KOLOM_ASLI] = df[NOMINAL_KOLOM_ASLI].str.replace(r'[^\d.-]', '', regex=True)
    df[NOMINAL_KOLOM_ASLI] = pd.to_numeric(df[NOMINAL_KOLOM_ASLI], errors='coerce').fillna(0)

    # 3. Pembersihan BBM & KM
    for target_col in [BBM_KOLOM_ASLI, KM_KOLOM_ASLI]:
        if target_col in df.columns:
            df[target_col] = df[target_col].astype(str).str.replace(r'[^\d.-]', '', regex=True)
            df[target_col] = pd.to_numeric(df[target_col], errors='coerce').fillna(0)

    # Perhitungam Rasio BBM per KM
    if BBM_KOLOM_ASLI in df.columns and KM_KOLOM_ASLI in df.columns:
        df['BBM per KM (L/KM)'] = np.where(df[KM_KOLOM_ASLI] > 0, (df[BBM_KOLOM_ASLI] / df[KM_KOLOM_ASLI]), 0).round(3)
    else:
        df['BBM per KM (L/KM)'] = 0.0

    # 4. Audit AI Kewajaran Finansial
    median_ops = df[NOMINAL_KOLOM_ASLI].median() if df[NOMINAL_KOLOM_ASLI].median() > 0 else 500000
    def cek_kewajaran(row):
        nominal = row[NOMINAL_KOLOM_ASLI]
        if nominal == 0:
            return "⚠️ Format Data Salah / Nol"
        elif nominal > (median_ops * 3):
            return "🚨 Tinggi (Perlu Review)"
        elif nominal > (median_ops * 1.5):
            return "🟡 Wajar (Di Atas Rata-rata)"
        else:
            return "🟢 Sangat Wajar"

    df['Analisa Kewajaran'] = df.apply(cek_kewajaran, axis=1)

    # Amankan kolom filter dari tipe non-string
    for c in [PIC_KOLOM_ASLI, TAHAP_KOLOM_ASLI, TIM_KOLOM_ASLI]:
        if c in df.columns: 
            df[c] = df[c].astype(str).str.strip().replace('nan', '').fillna('')

    # --- SIDEBAR FILTER ---
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

    if 'Bulan' in df.columns and not df['Bulan'].isna().all():
        unique_bulan = ["Semua Bulan"] + sorted([x for x in df['Bulan'].dropna().unique() if x])
        selected_bulan = st.sidebar.selectbox("📅 Pilih Bulan", unique_bulan)
    else:
        selected_bulan = "Semua Bulan"

    if st.sidebar.button("🔄 Reset Semua Filter & Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # --- PROSES FILTERING ---
    df_filtered = df.copy()
    if search_pic and PIC_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[PIC_KOLOM_ASLI].str.contains(search_pic, case=False, na=False)]
    if selected_tim != "Semua Tim" and TIM_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TIM_KOLOM_ASLI] == selected_tim]
    if selected_tahap != "Semua Tahap" and TAHAP_KOLOM_ASLI in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[TAHAP_KOLOM_ASLI] == selected_tahap]
    if selected_bulan != "Semua Bulan":
        df_filtered = df_filtered[df_filtered['Bulan'] == selected_bulan]

    # --- TAMPILAN UTAMA ---
    st.title("💳 Financial & Fuel Analytics Dashboard")
    st.caption("Monitoring Real-Time Pengeluaran Keuangan & Audit Konsumsi BBM Operasional")
    st.markdown("---")

    # --- METRICS CARD ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered[NOMINAL_KOLOM_ASLI].sum()
    avg_bbm = df_filtered['BBM per KM (L/KM)'].mean() if total_transaksi > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Biaya Operasional", value=f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Rasio BBM", value=f"{avg_bbm:.3f} L / KM")
    with col3:
        st.metric(label="Jumlah Log Terhitung", value=f"{total_transaksi} Item")

    st.markdown("---")

    # --- GRAFIK KOMPARASI BBM ---
    st.subheader("📊 Grafik Komparasi Kewajaran Operasional vs Konsumsi BBM")
    if not df_filtered.empty and total_pengeluaran > 0:
        chart_idx = df_filtered[PIC_KOLOM_ASLI].values if PIC_KOLOM_ASLI in df_filtered.columns else range(1, len(df_filtered)+1)
        compare_df = pd.DataFrame({
            'Total Biaya Ops': df_filtered[NOMINAL_KOLOM_ASLI].values,
            'Rasio BBM L/KM (Skala x100k)': df_filtered['BBM per KM (L/KM)'].values * 100000 
        }, index=chart_idx)
        st.bar_chart(compare_df, color=["#3b82f6", "#ef4444"])
    else:
        st.warning("💡 Grafik Utama tidak muncul karena Total Biaya terhitung masih Rp 0. Periksa setelan nama KOLOM ASLI di baris 32.")

    st.markdown("---")

    # --- GRAFIK PENDUKUNG ---
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.subheader("📅 Tren Alokasi Dana per Bulan")
        if not df_filtered.empty and total_pengeluaran > 0:
            st.line_chart(df_filtered.groupby('Tahun-Bulan')[NOMINAL_KOLOM_ASLI].sum(), color="#10b981")
    with col_sub2:
        st.subheader("👥 Distribusi Anggaran per Tim")
        if not df_filtered.empty and TIM_KOLOM_ASLI in df_filtered.columns and total_pengeluaran > 0:
            st.bar_chart(df_filtered.groupby(TIM_KOLOM_ASLI)[NOMINAL_KOLOM_ASLI].sum(), color="#f59e0b")

    st.markdown("---")

    # --- TABEL DATA ---
    st.subheader("📋 Rincian Data Log & Analisa Kewajaran")
    if not df_filtered.empty:
        df_display = df_filtered.copy()
        
        # Urutan kolom tabel
        base_cols = ['Analisa Kewajaran', 'BBM per KM (L/KM)', NOMINAL_KOLOM_ASLI, 'Teks_Asli_Nota']
        cols_to_show = base_cols + [c for c in df_display.columns if c not in base_cols and c not in ['Bulan', 'Tahun-Bulan']]
        df_display = df_display[cols_to_show]
        
        # Formatting visual rupiah
        df_display[NOMINAL_KOLOM_ASLI] = df_display[NOMINAL_KOLOM_ASLI].map("Rp {:,.0f}".format)
        if TANGGAL_KOLOM_ASLI in df_display.columns:
            df_display[TANGGAL_KOLOM_ASLI] = df_display[TANGGAL_KOLOM_ASLI].dt.strftime('%Y-%m-%d').fillna('-')
        df_display['BBM per KM (L/KM)'] = df_display['BBM per KM (L/KM)'].map("{:.3f} L/KM".format)

        st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.info("Mencoba mengunduh file spreadsheet...")
