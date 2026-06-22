import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS CARD DESIGN ---
st.markdown("""
    <style>
    /* Styling tombol agar menjadi Kartu 3D Besar */
    div.stButton > button {
        width: 100% !important;
        height: 250px !important; /* Ukuran lebih besar */
        border-radius: 25px !important;
        border: none !important;
        background: linear-gradient(145deg, #2d303e, #262730) !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    div.stButton > button:hover {
        transform: translateY(-15px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
        background: linear-gradient(145deg, #3d4156, #353748) !important;
        border: 1px solid #6c63ff !important;
    }
    .big-icon { font-size: 80px !important; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("<br>", unsafe_allow_html=True)
    
    menus = [
        ("💰", "Varcost", "Monitoring Varcost"),
        ("🎯", "KPI", "Monitoring KPI"),
        ("🔧", "Maintenance", "Monitoring Preventive Maintenance"),
        ("🏢", "Asset", "Monitoring Asset"),
        ("🚀", "Project", "Monitoring Project"),
        ("⚙️", "Operational", "Monitoring Operational")
    ]
    
    cols = st.columns(3)
    for i, (icon, label, target) in enumerate(menus):
        with cols[i % 3]:
            # Tombol langsung menjalankan navigasi tanpa penghalang
            if st.button(f"<div class='big-icon'>{icon}</div>{label}", key=label):
                navigate_to(target)
    
elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali ke Dashboard"): navigate_to("Halaman Depan")
    st.markdown("---")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT akan tampil di sini.")
    with tab2: st.write("Data Asset Rental akan tampil di sini.")

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Dashboard"): navigate_to("Halaman Depan")
    st.markdown("---")
    st.write(f"Konten detail untuk {st.session_state.current_page} sedang dimuat...")
