import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS PRESISI MUTLAK ---
st.markdown("""
    <style>
    /* 1. Grid Container agar 3 kolom selalu sejajar */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        padding: 20px;
    }
    
    /* 2. Kartu (Box) dengan ukuran yang dikunci */
    .menu-card {
        height: 220px !important; /* Ukuran tinggi tetap */
        background: linear-gradient(145deg, #2d303e, #262730);
        border-radius: 20px;
        border: 1px solid #444;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    .menu-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        border: 1px solid #6c63ff;
    }

    /* 3. Tombol Transparan menutupi seluruh kotak agar bisa diklik */
    div.stButton > button {
        position: absolute;
        width: 100% !important;
        height: 100% !important;
        opacity: 0;
        cursor: pointer;
    }
    
    .icon-text { font-size: 50px; }
    .label-text { font-size: 18px; font-weight: bold; color: white; margin-top: 10px; }
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
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    for icon, label, target in menus:
        # Kita buat kolom virtual di dalam HTML agar bisa di-grid
        # Namun karena Streamlit butuh state, kita taruh button di setiap item
        with st.container():
            st.markdown(f"""
                <div class="menu-card">
                    <div class="icon-text">{icon}</div>
                    <div class="label-text">{label}</div>
                </div>
            """, unsafe_allow_html=True)
            # Tombol transparan menutupi kartu
            if st.button(f"Klik {label}", key=target):
                navigate_to(target)
                
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page.startswith("Monitoring"):
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
