import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# CSS untuk membuat kartu yang bisa diklik seluruh area-nya
st.markdown("""
    <style>
    .card-container {
        position: relative;
        height: 200px;
        background: #262730;
        border-radius: 15px;
        border: 1px solid #444;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: 0.3s;
    }
    .card-container:hover { border-color: #6c63ff; transform: translateY(-5px); }
    .card-icon { font-size: 50px; margin-bottom: 10px; }
    .card-text { font-size: 18px; font-weight: bold; color: white; }
    
    /* Tombol transparan menutupi seluruh kartu */
    div.stButton > button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0; cursor: pointer;
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
            # Membuat kartu dengan posisi relative
            st.markdown(f"""
                <div class="card-container">
                    <div class="card-icon">{icon}</div>
                    <div class="card-text">{title}</div>
                </div>
            """, unsafe_allow_html=True)
            # Tombol diletakkan di atas kartu (transparan)
            if st.button(f"Klik {title}", key=title):
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
