import streamlit as st

st.set_page_config(page_title="Dashboard Profesional", layout="wide")

# --- CSS PROFESIONAL (GLASSMORPHISM) ---
st.markdown("""
    <style>
    .dashboard-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-top: 30px;
        flex-wrap: wrap;
    }
    .menu-item {
        flex: 1;
        min-width: 140px;
        height: 160px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
        text-decoration: none;
        color: white;
        cursor: pointer;
    }
    .menu-item:hover {
        background: rgba(108, 99, 255, 0.2);
        border-color: #6c63ff;
        transform: translateY(-10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .icon { font-size: 40px; margin-bottom: 10px; }
    .label { font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Kinarya Utama Teknik Dashboard")
    st.markdown("---")
    
    menus = [
        ("💰", "VARCOST"), ("🎯", "KPI"), ("🔧", "MAINTENANCE"),
        ("🏢", "ASSET"), ("🚀", "PROJECT"), ("⚙️", "OPERATIONAL")
    ]
    
    # Membuat baris menu
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Kita gunakan kolom kosong atau loop untuk membuat elemen yang bisa diklik
    # Agar bisa diklik di Streamlit, kita gunakan st.button dalam bentuk tombol transparan
    # yang ditaruh di atas div kartu (ini teknik rahasia desain web)
    
    cols = st.columns(6)
    for i, (icon, label) in enumerate(menus):
        with cols[i]:
            # Membuat area kartu yang bisa diklik
            if st.button(f"{icon}\n\n{label}", key=label):
                navigate_to(f"Monitoring {label.capitalize()}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page.startswith("Monitoring"):
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
