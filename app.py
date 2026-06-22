import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfigurasi Halaman & Tema Gelap ala Telco Ops Center
st.set_page_config(
    page_title="Telco Corporate Dashboard", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inisialisasi session state untuk navigasi halaman
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "VARCOST"

# ==========================================
# 2. NAVIGASI ATAS (PRESISI & INSTAN)
# ==========================================
col1, col2, col3, col4, col5, col6 = st.columns(6)

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

st.markdown("---")

# ==========================================
# 3. KONTEN HALAMAN (TAMPILAN TELEKOMUNIKASI)
# ==========================================

# --- HALAMAN UTAMA / DEFAULT (VARCOST TELCO) ---
def halaman_varcost():
    st.title("🌐 Telecom Variable Cost Analysis")
    st.caption("Memantau fluktuasi biaya operasional jaringan, interkoneksi, dan infrastruktur telekomunikasi.")
    st.write("")

    # Baris 1: Ringkasan Metrik Finansial Utama
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
    
    # Baris 2: Grafik Tren dan Detail Data
    g1, g2 = st.columns([2, 1])
    
    with g1:
        st.subheader("📈 Monthly Variable Cost Trend (2026)")
        # Membuat data simulasi tren biaya jaringan bulanan
        chart_data = pd.DataFrame(
            {
                "IP Transit":,
                "BTS Fuel & Power":,
                "Fiber Lease Leased Lines": [95, 95, 98, 102, 100, 105]
            },
            index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        )
        st.line_chart(chart_data)
        
    with g2:
        st.subheader("📊 Regional Allocation")
        # Distribusi biaya berdasarkan region operasional
        region_data = pd.DataFrame({
            "Region": ["Jabodetabek", "Sumatera", "Jawa Tengah", "Jawa Timur", "Kalimantan", "Sulawesi"],
            "Cost (IDR B)": [45.2, 28.4, 22.1, 26.8, 18.5, 14.2]
        })
        st.dataframe(region_data, use_container_width=True, hide_index=True)

# --- HALAMAN LAIN (DUMMY PLACEHOLDER) ---
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
