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

# Memuat Data Otomatis dengan Anti-Cache (TTL 5 detik)
@st.cache_data(ttl=5)
def load_financial_data(url):
    try:
        df = pd.read_csv(f"{url}&timestamp={pd.Timestamp.now().timestamp()}")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari sheet Detail OPS. Pastikan link sudah 'Anyone with link can view'. Error: {e}")
        return None

df_raw = load_financial_data(csv_url)

if df_raw is not None and not df_raw.empty:
    # Bersihkan kolom kosong akibat pembacaan gviz
    df = df_raw.dropna(how='all', axis=1).copy()
    cols = df.columns
    
    # --- MAPPING KOLOM SECARA DINAMIS (Anti-Error Huruf Besar/Kecil) ---
    pic_col = next((c for c in cols if 'pic' in c.lower() or 'request' in c.lower()), None)
    tahap_col = next((c for c in cols if 'tahap' in c.lower() or 'status' in c.lower()), None)
    tanggal_col = next((c for c in cols if 'tanggal' in c.lower() or 'date' in c.lower()), None)
    tim_col = next((c for c in cols if 'tim' in c.lower() or 'team' in c.lower() or 'divisi' in c.lower()), None)
    
    # Kolom nominal (Total Biaya Sesuai Nota)
    nominal_col = next((c for c in cols if any(k in c.lower() for k in ['nota', 'nominal', 'jumlah', 'biaya', 'amount', 'total'])), None)

    # --- PRE-PROCESSING DATA ---
    # 1. Standarisasi Tanggal & Urutan Bulan
    if tanggal_col:
        df[tanggal_col] = pd.to_datetime(df[tanggal_col], errors='coerce', format='mixed')
        df['Bulan'] = df[tanggal_col].dt.strftime('%B')
        df['Tahun-Bulan'] = df[tanggal_col].dt.strftime('%Y-%m')
    else:
        df['Bulan'] = "Tidak Ada Data Tanggal"
        df['Tahun-Bulan'] = "Tidak Ada Data Tanggal"

    # 2. Pembersihan Data Finansial (Sangat Agresif)
    if nominal_col:
        # Jika berupa string/objek, hapus Rp, titik ribuan, spasi, dan karakter non-angka lainnya
        if df[nominal_col].dtype == object:
            df[nominal_col] = df[nominal_col].astype(str).str.replace('Rp', '', regex=False)
            df[nominal_col] = df[nominal_col].str.replace('.', '', regex=False)  # Hapus titik ribuan Indonesia
            df[nominal_col] = df[nominal_col].str.replace(',', '.', regex=False)  # Ubah koma desimal ke titik desimal
            df[nominal_col] = df[nominal_col].str.replace(r'[^\d.-]', '', regex=True) # Hapus sisa karakter aneh
        df[nominal_col] = pd.to_numeric(df[nominal_col], errors='coerce').fillna(0)
    else:
        df['Nominal_Clean'] = 0
        nominal_col = 'Nominal_Clean'

    # 3. Kolom Analisa Kewajaran Operasional (Rule-Based AI)
    # Membuat penilaian otomatis berdasarkan rata-rata pengeluaran log saat ini
    rerata_kondisi = df[nominal_col].median() if df[nominal_col].median() > 0 else 500000
    
    def cek_kewajaran(row):
        nominal = row[nominal_col]
        if nominal == 0:
            return "⚠️ Data Kosong / Belum Diinput"
        elif nominal > (rerata_kondisi * 3):
            return "🚨 Tinggi (Perlu Review Tambahan)"
        elif nominal > (rerata_kondisi * 1.5):
            return "🟡 Wajar (Di Atas Rata-rata)"
        else:
            return "🟢 Sangat Wajar / Sesuai Budget"

    df['Analisa Kewajaran'] = df.apply(cek_kewajaran, axis=1)

    # Pastikan data string filter aman dari nilai kosong/NaN
    for c in [pic_col, tahap_col, tim_col]:
        if c: df[c] = df[c].astype(str).str.strip().replace('nan', '').fillna('')

    # --- SIDEBAR FILTER (TERINTEGRASI PENUH) ---
    st.sidebar.header("⚙️ Panel Filter Analisa")
    
    # Filter 1: Pencarian Teks PIC / Requestor
    search_pic = st.sidebar.text_input("👤 Cari PIC / Requestor", placeholder="Ketik nama...")
    
    # Filter 2: Dropdown Tim (Terintegrasi)
    if tim_col and df[tim_col].str.len().sum() > 0:
        unique_tim = ["Semua Tim"] + sorted([x for x in df[tim_col].unique() if x])
        selected_tim = st.sidebar.selectbox("👥 Pilih Tim", unique_tim)
    else:
        selected_tim = "Semua Tim"
    
    # Filter 3: Dropdown Tahap
    if tahap_col:
        unique_tahap = ["Semua Tahap"] + sorted([x for x in df[tahap_col].unique() if x])
        selected_tahap = st.sidebar.selectbox("🔄 Pilih Tahap", unique_tahap)
    else:
        selected_tahap = "Semua Tahap"

    # Filter 4: Dropdown Bulan (Terintegrasi)
    if tanggal_col and not df['Bulan'].isna().all():
        unique_bulan = ["Semua Bulan"] + sorted([x for x in df['Bulan'].dropna().unique() if x])
        selected_bulan = st.sidebar.selectbox("📅 Pilih Bulan", unique_bulan)
    else:
        selected_bulan = "Semua Bulan"

    if st.sidebar.button("🔄 Reset Semua Filter", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # --- PROSES FILTERING DATA MULTI-DIMENSI ---
    df_filtered = df.copy()
    if search_pic and pic_col:
        df_filtered = df_filtered[df_filtered[pic_col].str.contains(search_pic, case=False, na=False)]
    if selected_tim != "Semua Tim" and tim_col:
        df_filtered = df_filtered[df_filtered[tim_col] == selected_tim]
    if selected_tahap != "Semua Tahap" and tahap_col:
        df_filtered = df_filtered[df_filtered[tahap_col] == selected_tahap]
    if selected_bulan != "Semua Bulan":
        df_filtered = df_filtered[df_filtered['Bulan'] == selected_bulan]

    # --- TAMPILAN UTAMA DASHBOARD ---
    st.title("💳 Financial Operations Dashboard")
    st.caption("Analisa Real-Time Pengeluaran & Anggaran Operasional Finansial (Sheet: Detail OPS)")
    st.info("🔄 Dashboard terintegrasi penuh. Perubahan filter di samping akan langsung memperbarui grafik & angka total.")
    st.markdown("---")

    # --- CARD KPI UTAMA ---
    total_transaksi = len(df_filtered)
    total_pengeluaran = df_filtered[nominal_col].sum()
    rata_rata_biaya = df_filtered[nominal_col].mean() if total_transaksi > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Biaya Sesuai Nota (Terfilter)", value=f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
    with col2:
        st.metric(label="Rata-rata Biaya Operasional", value=f"Rp {rata_rata_biaya:,.0f}".replace(",", "."))
    with col3:
        st.metric(label="Jumlah Log / Nota Terhitung", value=f"{total_transaksi} Item")

    st.markdown("---")

    # --- BAGIAN GRAFIK ANALISA TERINTEGRASI ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📊 Tren Alokasi Dana per Bulan")
        if not df_filtered.empty and tanggal_col:
            # Menggunakan Tahun-Bulan atau Bulan sebagai indeks grafik
            trend_data = df_filtered.groupby('Tahun-Bulan')[nominal_col].sum()
            st.line_chart(trend_data, color="#10b981") 
        else:
            st.info("Data tidak cukup untuk menampilkan grafik tren.")

    with col_chart2:
        st.subheader("👥 Distribusi Anggaran per Tim / Divisi")
        if not df_filtered.empty and tim_col:
            tim_chart_data = df_filtered.groupby(tim_col)[nominal_col].sum().sort_values(ascending=False)
            st.bar_chart(tim_chart_data, color="#3b82f6") 
        else:
            st.info("Sistem tidak mendeteksi data kolom Tim untuk dirender ke grafik.")

    st.markdown("---")

    # --- TABEL LOG DETAIL DENGAN KOLOM ANALISA KEWAJARAN ---
    st.subheader("📋 Rincian Data Log & Analisa Kewajaran")
    
    if not df_filtered.empty:
        df_display = df_filtered.copy()
        
        # Pindahkan kolom Analisa Kewajaran ke depan agar mudah dianalisa
        cols_order = ['Analisa Kewajaran'] + [c for c in df_display.columns if c != 'Analisa Kewajaran' and c not in ['Bulan', 'Tahun-Bulan']]
        df_display = df_display[cols_order]
        
        # Format nominal rupiah untuk tampilan tabel agar cantik
        if nominal_col in df_display.columns:
            df_display[nominal_col] = df_display[nominal_col].map("Rp {:,.0f}".format)
        if tanggal_col in df_display.columns:
            df_display[tanggal_col] = df_display[tanggal_col].dt.strftime('%Y-%m-%d').fillna('-')

        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Data keuangan tidak ditemukan untuk kombinasi filter ini.")
else:
    st.info("Mencoba menyambungkan dan memproses data operasional dari sheet Anda...")
