import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS KARTU DIBUAT KOTAKNYA SAMA ---
st.markdown("""
    <style>
    .grid-wrapper {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-top: 20px;
    }
    .menu-box {
        height: 250px;
        wide : 300px;
        background: #262730;
        border-radius: 20px;
        border: 200px solid #444;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: 0.3s;
        cursor: pointer;
        color: white;
        text-decoration: none;
    }
    .menu-box:hover {
        border-color: #6c63ff;
        transform: translateY(-5px);
        background: #31333F;
    }
    .icon-part { font-size: 60px; margin-bottom: 10px; }
    .text-part { font-size: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("---")
    
    menus = [
        ("💰", "VARCOST", "Monitoring Varcost"),
        ("🎯", "KPI", "Monitoring KPI"),
        ("🔧", "MAINTENANCE", "Monitoring Maintenance"),
        ("🏢", "ASSET", "Monitoring Asset"),
        ("🚀", "PROJECT", "Monitoring Project"),
        ("⚙️", "OPERATIONAL", "Monitoring Operational")
    ]
    
    # Render Grid
    st.markdown('<div class="grid-container grid-wrapper">', unsafe_allow_html=True)
    
    # Menggunakan kolom untuk memicu event klik via tombol tersembunyi
    cols = st.columns(3)
    for i, (icon, label, target) in enumerate(menus):
        with cols[i % 3]:
            # Kita buat tombol yang memenuhi ruang untuk menangkap klik
            if st.button(f"{icon}\n\n{label}", key=target):
                navigate_to(target)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page.startswith("Monitoring"):
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
