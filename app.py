import streamlit as st
import pandas as pd
# import plotly.express as px # Nantinya digunakan untuk grafik/kurva

# Konfigurasi Halaman (Harus di baris paling atas)
st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# Membuat Sidebar untuk Menu Utama
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

# --- FUNGSI HALAMAN ---

if menu == "Halaman Depan":
    st.title("Selamat Datang di Corporate Dashboard")
    st.write("Silakan pilih menu di sidebar sebelah kiri untuk melihat detail monitoring.")
    st.info("Dashboard ini terintegrasi langsung dengan Google Sheets.")

elif menu == "1. Monitoring Varcost":
    st.title("Monitoring Varcost")
    st.subheader("Report Varcost")
    # TODO: Tarik data dari gsheets tab 'Varcost'
    st.write("Di sini akan ditampilkan tabel dan grafik berbagai report Varcost.")

elif menu == "2. Monitoring Preventive Maintenance":
    st.title("Monitoring Preventive Maintenance")
    st.subheader("Analisa Pencapaian & Kurva S")
    # TODO: Logika pembuatan Kurva S (biasanya membandingkan Plan vs Actual)
    st.write("Area untuk menampilkan Kurva S dari progres maintenance.")

elif menu == "3. Monitoring Project":
    st.title("Monitoring Project")
    st.subheader("Timeline & Status Project")
    # TODO: Gunakan Gantt Chart dengan Plotly untuk timeline
    st.write("Area untuk menampilkan daftar project dan timeline pengerjaan.")

elif menu == "4. Monitoring KPI":
    st.title("Monitoring KPI")
    st.subheader("Analisa & Perhitungan KPI")
    st.write("Area perhitungan bobot KPI dan pencapaian masing-masing divisi/karyawan.")

elif menu == "5. Monitoring Asset":
    st.title("Monitoring Asset (KUT, Kisel, Rental)")
    tab1, tab2, tab3 = st.tabs(["Asset KUT", "Asset Kisel", "Asset Rental"])
    
    with tab1:
        st.write("Data Asset KUT, Nilai Sewa, dan Depresiasi.")
    with tab2:
        st.write("Data Asset Kisel, Nilai Sewa, dan Depresiasi.")
    with tab3:
        st.write("Data Asset Rental, Nilai Sewa, dan Depresiasi.")

elif menu == "6. Monitoring Operational":
    st.title("Monitoring Operational")
    st.subheader("Analisa Konsumsi BBM")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total BBM Mobil", value="1.200 L") # Angka dummy
    with col2:
        st.metric(label="Total BBM Motor", value="450 L") # Angka dummy
    with col3:
        st.metric(label="Total BBM Genset", value="800 L") # Angka dummy
        
    st.write("Tabel detail operasional akan muncul di bawah sini.")

elif menu == "7. Monitoring PJB":
    st.title("Monitoring PJB")
    st.subheader("Aging Berkas Pengajuan")
    # TODO: Logika kalkulasi hari masuk berkas vs hari ini (Aging)
    st.write("Daftar berkas yang melebihi batas waktu (SLA) akan disorot di sini.")