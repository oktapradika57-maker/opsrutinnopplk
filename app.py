import streamlit as st
import pandas as pd
# import plotly.express as px # Aktifkan nanti untuk membuat grafik

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# --- FUNGSI UNTUK MENARIK DATA DARI GOOGLE SHEETS ---
@st.cache_data(ttl=600) # Cache data selama 10 menit agar tidak membebani server
def load_data(sheet_name):
    # ID Spreadsheet Anda
    sheet_id = "1hIeT51_SVdNrz62s93zpZNyqepBMdNCa-mDRH-wVOIw"
    # Format URL untuk otomatis mengunduh sebagai CSV
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari sheet {sheet_name}. Pastikan nama sheet benar dan akses link terbuka.")
        return pd.DataFrame()

# --- SIDEBAR MENU ---
st.sidebar.title("Navigasi Dashboard")
menu = st.sidebar.radio(
    "Pilih Menu:",
    ["Halaman Depan", 
     "1. Monitoring Varcost", 
     "2. Monitoring Preventive Maintenance", 
     "3. Monitoring Project", 
     "4. Monitoring KPI", 
     "5. Monitoring Asset", 
     "6. Monitoring Operational", 
     "7. Monitoring PJB"]
)

# --- HALAMAN ---

if menu == "Halaman Depan":
    st.title("Selamat Datang di Corporate Dashboard")
    st.write("Silakan pilih menu di sidebar sebelah kiri.")

elif menu == "1. Monitoring Varcost":
    st.title("Monitoring Varcost")
    # Ganti 'NamaSheetVarcost' dengan nama tab asli di GSheets Anda
    df_varcost = load_data("NamaSheetVarcost") 
    if not df_varcost.empty:
        st.dataframe(df_varcost, use_container_width=True)

elif menu == "2. Monitoring Preventive Maintenance":
    st.title("Monitoring Preventive Maintenance")
    st.subheader("Data Pencapaian")
    
    # Contoh mengambil data dari sheet (misalnya nama tabnya 'SUMMARY')
    df_pm = load_data("SUMMARY")
    
    if not df_pm.empty:
        # Menampilkan tabel mentah
        st.dataframe(df_pm, use_container_width=True)
        
        # Contoh jika Anda ingin membuat metrik ringkasan
        # Pastikan nama kolom (seperti 'OPEN', 'DONE', 'TOTAL') sesuai dengan yang ada di Google Sheets Anda
        if 'TOTAL' in df_pm.columns and 'DONE' in df_pm.columns:
            total_target = df_pm['TOTAL'].sum()
            total_done = df_pm['DONE'].sum()
            
            col1, col2 = st.columns(2)
            col1.metric("Total PM Target", total_target)
            col2.metric("Total PM Done", total_done)
            
            # Area untuk Kurva S nantinya
            st.subheader("Kurva S PM")
            st.info("Untuk membuat Kurva S, pastikan di dalam dataset ada kolom 'Timeline/Bulan', 'Plan (%)', dan 'Actual (%)'.")

# ... (Menu 3 sampai 7 logikanya sama, Anda tinggal memanggil fungsi load_data("Nama_Tab_Di_Google_Sheets")) ...

elif menu == "7. Monitoring PJB":
    st.title("Monitoring PJB")
    st.write("Area Aging Berkas Pengajuan")
