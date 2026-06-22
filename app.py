import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# CSS untuk kartu yang bisa diklik seluruh areanya
st.markdown("""
    <style>
    /* Styling agar tombol Streamlit mengisi seluruh area div */
    div.stButton > button {
        width: 100% !important;
        height: 200px !important;
        border-radius: 15px !important;
        border: 1px solid #444 !important;
        background-color: #262730 !important;
        color: white !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        border-color: #6c63ff !important;
        transform: translateY(-5px);
        background-color: #31333F !important;
    }
    .icon { font-size: 50px; margin-bottom: 10px; }
    .label { font-size: 18px; font-weight: bold; }
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
    for i, (icon, title, target) in enumerate(menus):
        with cols[i % 3]:
            # Tombol ini sekarang merender icon dan label di dalamnya
            # Pengguna bisa mengklik di mana saja dalam area kotak ini
            if st.button(f"<div class='icon'>{icon}</div><div class='label'>{title}</div>", key=title):
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
