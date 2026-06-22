import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# CSS untuk kartu yang rapi
st.markdown("""
    <style>
    .menu-card {
        background: #262730;
        border: 1px solid #444;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
    }
    .menu-card:hover { border-color: #6c63ff; transform: translateY(-5px); }
    .icon { font-size: 40px; margin-bottom: 10px; }
    .title { font-size: 18px; font-weight: bold; color: white; }
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
            # Membuat layout kartu menggunakan markdown
            st.markdown(f"""
                <div class="menu-card">
                    <div class="icon">{icon}</div>
                    <div class="title">{title}</div>
                </div>
            """, unsafe_allow_html=True)
            # Tombol diletakkan tepat di bawah/atas untuk aksi klik
            if st.button(f"Pilih {title}", key=title):
                navigate_to(target)
            st.markdown("<br>", unsafe_allow_html=True)

elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT...")
    with tab2: st.write("Data Asset Rental...")
else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
