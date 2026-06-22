import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# CSS untuk membuat tombol terlihat seperti kartu
st.markdown("""
    <style>
    /* Styling tombol agar lebih menarik */
    div.stButton > button {
        width: 100% !important;
        height: 180px !important;
        border-radius: 15px !important;
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
    }
    div.stButton > button:hover {
        border-color: #6c63ff !important;
        transform: translateY(-5px);
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
    
    # Daftar Menu dengan Emoji sebagai Icon (pasti muncul)
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
            # Kita gunakan format emoji + label agar pasti tampil
            if st.button(f"{icon}\n\n{label}", key=label):
                navigate_to(target)
            st.write("") # Memberi jarak

elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT...")
    with tab2: st.write("Data Asset Rental...")
else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
