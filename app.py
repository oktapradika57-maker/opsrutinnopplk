import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS PRESISI LANDSCAPE ---
st.markdown("""
    <style>
    /* Memastikan tombol memiliki ukuran tetap yang sama */
    div.stButton > button {
        width: 100% !important;
        height: 150px !important; 
        border-radius: 15px !important;
        border: 2px solid #444 !important;
        background: #262730 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        border-color: #6c63ff !important;
        background: #31333F !important;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("---")
    
    # Daftar menu
    menus = [
        ("💰", "VARCOST"), ("🎯", "KPI"), ("🔧", "MAINTENANCE"),
        ("🏢", "ASSET"), ("🚀", "PROJECT"), ("⚙️", "OPERATIONAL")
    ]
    
    # MENGUBAH TAMPILAN MENJADI LANDSCAPE DENGAN 6 KOLOM
    cols = st.columns(6)
    
    for i, (icon, label) in enumerate(menus):
        # Setiap kolom hanya berisi 1 tombol, sehingga berjejer ke samping (Landscape)
        with cols[i]:
            if st.button(f"{icon}\n\n{label}", key=label):
                navigate_to(f"Monitoring {label.capitalize()}")

elif st.session_state.current_page.startswith("Monitoring"):
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Dashboard"): navigate_to("Halaman Depan")
