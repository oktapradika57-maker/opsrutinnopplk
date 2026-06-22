import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS CARD DESIGN ---
st.markdown("""
    <style>
    /* Styling tombol agar menjadi Kartu 3D Besar */
    div.stButton > button {
        width: 150% !important;
        height: 250px !important; 
        border-radius: 250px !important;
        border: none !important;
        background: linear-gradient(145deg, #2d303e, #262730) !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-15px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
        background: linear-gradient(145deg, #3d4156, #353748) !important;
        border: 1px solid #6c63ff !important;
    }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gunakan format teks standar Streamlit agar ikon (emoji) dan tulisan muncul
    menus = [
        ("💰\n\nVARCOST", "Monitoring Varcost"),
        ("🎯\n\nKPI", "Monitoring KPI"),
        ("🔧\n\nMAINTENANCE", "Monitoring Preventive Maintenance"),
        ("🏢\n\nASSET", "Monitoring Asset"),
        ("🚀\n\nPROJECT", "Monitoring Project"),
        ("⚙️\n\nOPERATIONAL", "Monitoring Operational")
    ]
    
    cols = st.columns(3)
    for i, (label, target) in enumerate(menus):
        with cols[i % 3]:
            # Tombol ini pasti menampilkan ikon dan tulisan karena formatnya valid
            if st.button(label, key=target):
                navigate_to(target)
    
elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali ke Dashboard"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT...")
    with tab2: st.write("Data Asset Rental...")

else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Dashboard"): navigate_to("Halaman Depan")
    st.write(f"Konten detail untuk {st.session_state.current_page} sedang dimuat...")
