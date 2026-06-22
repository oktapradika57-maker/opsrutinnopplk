import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# --- CSS PRESISI MUTLAK ---
st.markdown("""
    <style>
    /* Mengunci ukuran tombol agar tidak peduli isi teksnya */
    div.stButton > button {
        width: 100% !important;
        height: 180px !important; /* Tinggi tetap */
        border-radius: 20px !important;
        border: 2px solid #555 !important;
        background-color: #262730 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: 0.3s !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    div.stButton > button:hover { border-color: #6c63ff !important; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("---")
    
    # List menu
    menus = [
        ("💰", "Varcost", "Monitoring Varcost"),
        ("🎯", "KPI", "Monitoring KPI"),
        ("🔧", "Maintenance", "Monitoring Preventive Maintenance"),
        ("🏢", "Asset", "Monitoring Asset"),
        ("🚀", "Project", "Monitoring Project"),
        ("⚙️", "Operational", "Monitoring Operational")
    ]
    
    # Menggunakan columns dengan lebar yang sama rata (3 kolom)
    cols = st.columns([1, 1, 1])
    
    for i, (icon, label, target) in enumerate(menus):
        col_idx = i % 3
        with cols[col_idx]:
            # Menggunakan string yang disatukan agar tombol tidak melebar secara dinamis
            btn_text = f"{icon}  \n  {label}"
            if st.button(btn_text, key=label):
                navigate_to(target)
            st.write("") # Spasi bawah

elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT...")
    with tab2: st.write("Data Asset Rental...")
else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
