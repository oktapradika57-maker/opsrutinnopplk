import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# --- CSS CARD DESIGN ---
st.markdown("""
    <style>
    /* Styling tombol agar berbentuk kartu */
    div.stButton > button {
        width: 100% !important;
        height: 220px !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: linear-gradient(145deg, #2a2d3e, #1e202b) !important;
        color: white !important;
        transition: 0.3s !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    div.stButton > button:hover {
        transform: translateY(-10px);
        border: 1px solid #6c63ff !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .icon-style { font-size: 50px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Definisi menu (Ikon, Nama, Target)
    menus = [
        ("💰", "Varcost", "Monitoring Varcost"),
        ("🎯", "KPI", "Monitoring KPI"),
        ("🔧", "Maintenance", "Monitoring Preventive Maintenance"),
        ("🏢", "Asset", "Monitoring Asset"),
        ("🚀", "Project", "Monitoring Project"),
        ("⚙️", "Operational", "Monitoring Operational")
    ]
    
    cols = st.columns(3)
    for i, (icon, title, target) in enumerate(menus):
        with cols[i % 3]:
            # Tombol berfungsi langsung saat diklik
            if st.button(f"<div class='icon-style'>{icon}</div><div style='font-size:18px;'>{title}</div>", key=title):
                navigate_to(target)

elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT...")
    with tab2: st.write("Data Asset Rental...")

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    st.write(f"Halaman {st.session_state.current_page} sedang dimuat.")
