import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & Tema Gelap ala Telco Ops Center
st.set_page_config(
    page_title="Telco Corporate Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inisialisasi session state untuk navigasi halaman jika belum ada
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST"

# ==========================================
# 2. NAVIGASI ATAS (8 MENU PRESISI & INSTAN)
# ==========================================
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    if st.button("💰\n\nVARCOST", use_container_width=True, key="btn_varcost"):
        st.session_state.active_menu = "VARCOST"
        st.rerun()

with col2:
    if st.button("📈\n\nKPI", use_container_width=True, key="btn_kpi"):
        st.session_state.active_menu = "KPI"
        st.rerun()

with col3:
    if st.button("🛠️\n\nMAINTENANCE", use_container_width=True, key="btn_maint"):
        st.session_state.active_menu = "MAINTENANCE"
        st.rerun()

with col4:
    if st.button("🏢\n\nASSET", use_container_width=True, key="btn_asset"):
        st.session_state.active_menu = "ASSET"
        st.rerun()

with col5:
    if st.button("🚀\n\nPROJECT", use_container_width=True, key="btn_project"):
        st.session_state.active_menu = "PROJECT"
        st.rerun()

with col6:
    if st.button("⚙️\n\nOPERATIONAL", use_container_width=True, key="btn_operational"):
        st.session_state.active_menu = "OPERATIONAL"
        st.rerun()

with col7:
    if st.button("📡\n\nMONITORING MBP", use_container_width=True, key="btn_mbp"):
        st.session_state.active_menu = "MONITORING_MBP"
        st.rerun()

with col8:
    if st.button("📋\n\nPROGRESS MATELINE", use_container_width=True, key="btn_mateline"):
        st.session_state.active_menu = "PROGRESS_MATELINE"
        st.rerun()

st.markdown("---")

# ==========================================
# 3. KONTEN HALAMAN (TAMPILAN TELEKOMUNIKASI)
# ==========================================

# --- HALAMAN UTAMA (VARCOST TELCO + DROPDOWN ANALISA FINANSIAL) ---
def halaman_varcost():
    st.title("🌐 Telecom Variable Cost & Financial Analysis")
    st.caption("Memantau fluktuasi biaya operasional jaringan, interkoneksi, serta kinerja finansial korporat.")
    st.write("")

    # Dropdown Analisa Finansial (Revenue & Income)
    st.subheader("📊 Corporate Financial Analysis")
    opsi_analisa = st.selectbox(
        "Pilih Metrik Analisis Finansial:",
        ["Revenue Analysis (Pendapatan)", "Net Income Analysis (Laba Bersih)"]
    )

    # Logika Tampilan Berdasarkan Dropdown
    if opsi_analisa == "Revenue Analysis (Pendapatan)":
        r1, r2 = st.columns(2)
        with r1:
            st.info("📈 **Tren Pendapatan Korporat (Berdasarkan Lini Bisnis)**")
            data_rev = pd.DataFrame({
                "Mobile Data (Cellular)": [7.2, 7.3, 7.5, 7.4, 7.6, 7.8],
                "FTTH & Broadband": [4.1, 4.2, 4.3, 4.3, 4.5, 4.6],
                "Enterprise Solution": [1.5, 1.6, 1.6, 1.7, 1.7, 1.8]
            }, index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
            st.line_chart(data_rev)
        with r2:
            st.metric(label="Total Revenue Q2 2026", value="IDR 14.2 Triliun", delta="+6.4% YoY")
            st.write("")
            st.caption("**Kontributor Terbesar:** Layanan Data Seluler tetap mendominasi pendapatan sebesar 52%.")

    elif opsi_analisa == "Net Income Analysis (Laba Bersih)":
        i1, i2 = st.columns(2)
        with i1:
            st.success("💰 **Tren Laba Bersih Perusahaan (2026)**")
            data_inc = pd.DataFrame({
                "Net Income (Miliar IDR)": [1200, 1250, 1310, 1280, 1340, 1410]
            }, index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
            st.bar_chart(data_inc)
        with i2:
            st.metric(label="Net Profit Margin (NPM)", value="14.8 %", delta="+1.2% MoM")
            st.write("")
            st.caption("**Catatan Finansial:** Kenaikan laba bersih bulan Juni didorong oleh efisiensi biaya energi pada BTS.")

    st.markdown("---")

    # Baris Ringkasan Metrik Finansial Utama (Varcost)
    st.subheader("💸 Operational Variable Cost Summary")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Bandwidth Transit Cost", value="$423,500", delta="-4.2% MoM")
    with m2:
        st.metric(label="Network Energy Cost (BTS)", value="$1,240,800", delta="+8.1% MoM", delta_color="inverse")
    with m3:
        st.metric(label="Interconnection / Roaming Fees", value="$315,200", delta="-1.5% MoM")
    with m4:
        st.metric(label="Outsourced Field Ops Cost", value="$189,400", delta="Stable")

    st.write("")
    
    # Baris Detail Data Regional (Grafik Bulanan IP Transit yang error sudah dibuang)
    st.subheader("📊 Regional Cost Allocation")
    region_data = pd.DataFrame({
        "Region": ["Jabodetabek", "Sumatera", "Jawa Tengah", "Jawa Timur", "Kalimantan", "Sulawesi"],
        "Cost (IDR B)": [45.2, 28.4, 22.1, 26.8, 18.5, 14.2]
    })
    st.dataframe(region_data, use_container_width=True, hide_index=True)

# --- HALAMAN MENU LAIN ---
def halaman_kpi():
    st.title("📈 Telecom Network KPI")
    st.info("Metrik Performa: Dropped Call Rate (DCR), Call Setup Success Rate (CSSR), Network Availability (99.98%), & Average Throughput.")

def halaman_maintenance():
    st.title("🛠️ Preventive & Corrective Maintenance")
    st.warning("Jadwal Perawatan: Penggantian Baterai Lithium BTS, Kalibrasi Perangkat Microwave, dan Perbaikan Kabel Fiber Optik (Cut).")

def halaman_asset():
    st.title("🏢 Telecom Asset Inventory")
    st.write("Manajemen Aset: Menampilkan daftar Menara (Tower), Core Router, Spectrum Licenses, dan Data Center Facility.")

def halaman_project():
    st.title("🚀 Network Rollout & Project Deployment")
    st.write("Status Proyek: Pemetaan Ekspansi Jaringan 5G Standalone (SA) dan Implementasi FTTH (Fiber to the Home).")

def halaman_operational():
    st.title("⚙️ Network Operations Center (NOC)")
    st.write("Operasional Lapangan: Monitoring Traffic Load, Manajemen Tiket Gangguan, dan Utilisasi Kapasitas Server.")

# --- HALAMAN MONITORING MBP ---
def halaman_monitoring_mbp():
    st.title("📡 Monitoring MBP (Mobile Backup Power)")
    st.caption("Memantau status ketersediaan dan lokasi genset mobile / baterai backup cadangan saat terjadi pemadaman listrik PLN di site BTS.")
    
    s1, s2, s3 = st.columns(3)
    s1.metric("Total Unit MBP Aktif", "142 Unit", "Beroperasi")
    s2.metric("Unit On Standby / Ready", "58 Unit", "Siaga")
    s3.metric("Critical Site (No Backup)", "3 Site", "⚠️ Butuh Deployment", delta_color="inverse")
    
    st.subheader("📋 Realtime Deployment List MBP")
    mbp_data = pd.DataFrame({
        "ID Unit MBP": ["MBP-REG1-042", "MBP-REG1-089", "MBP-REG2-011", "MBP-REG3-102"],
        "Target Site ID": ["JKT_ANGKREK02", "BKS_TAMBUN05", "BDG_DAGO_CORE", "SBY_GUBENG01"],
        "Kapasitas KVA": ["50 KVA", "35 KVA", "100 KVA", "50 KVA"],
        "Sisa Bahan Bakar (BBM)": ["85%", "42%", "90%", "15% (Low)"],
        "Status Operasional": ["Dispatched & Active", "On Route", "Standby at Site", "Refueling Needed"]
    })
    st.dataframe(mbp_data, use_container_width=True, hide_index=True)

# --- HALAMAN PROGRESS MATELINE ---
def halaman_progress_mateline():
    st.title("📋 Progress Mateline & Material Management")
    st.caption("Pelacakan rantai pasok material infrastruktur jaringan kabel optik dan komponen menara telekomunikasi.")
    
    st.subheader("🚧 Material Procurement Progress")
    st.write("Kabel Fiber Optik Core 48 (Kebutuhan Rollout FTTH Jabar)")
    st.progress(0.85, text="85% Berhasil Didistribusikan ke Gudang Regional")
    
    st.write("Perangkat OLT (Optical Line Terminal) Huawei / ZTE")
    st.progress(0.60, text="60% Proses Custom Clearance di Pelabuhan")
    
    st.write("Tiang Pancang / Pole Antena 9 Meter")
    st.progress(0.35, text="35% Produksi di Pabrik Vendor Lokal")

# ==========================================
# 4. ROUTER EKSEKUSI HALAMAN
# ==========================================
if st.session_state.active_menu == "VARCOST":
    halaman_varcost()
elif st.session_state.active_menu == "KPI":
    halaman_kpi()
elif st.session_state.active_menu == "MAINTENANCE":
    halaman_maintenance()
elif st.session_state.active_menu == "ASSET":
    halaman_asset()
elif st.session_state.active_menu == "PROJECT":
    halaman_project()
elif st.session_state.active_menu == "OPERATIONAL":
    halaman_operational()
elif st.session_state.active_menu == "MONITORING_MBP":
    halaman_monitoring_mbp()
elif st.session_state.active_menu == "PROGRESS_MATELINE":
    halaman_progress_mateline()
