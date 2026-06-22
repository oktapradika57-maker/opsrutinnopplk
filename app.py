import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS PRESISI UNTUK LANDSCAPE ---
st.markdown("""
    <style>
    /* Membuat container grid untuk tata letak landscape */
    .landscape-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr); /* 6 kolom dalam 1 baris */
        gap: 15px;
        margin-top: 20px;
    }
    
    /* Mengunci ukuran box agar seragam */
    .menu-card {
        height: 180px; /* Tinggi seragam */
        background: #262730;
        border-radius: 15px;
        border: 2px solid #444;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: 0.3s;
        cursor: pointer;
        text-align: center;
    }
    .menu-card:hover {
        border-color: #6c63ff;
        background: #31333F;
        transform: translateY(-5px);
    }
    
    /* Menyembunyikan tombol Streamlit tapi tetap menjaga fungsinya */
    div.stButton > button {
        position: absolute;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: pointer;
    }
    
    .icon { font-size: 35px; }
    .label { font-size: 14px; font-weight: bold; color: white; margin-top: 8px; }
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
    
    # Render Landscape Grid
    st.markdown('<div class="landscape-grid">', unsafe_allow_html=True)
    
    for icon, label, target in menus:
        # Menggunakan kontainer agar tombol terikat pada box
        with st.container():
            st.markdown(f"""
                <div class="menu-card">
                    <div class="icon">{icon}</div>
                    <div class="label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
            # Tombol transparan diletakkan di atas box
            if st.button(f"Pilih {label}", key=target):
                navigate_to(target)
                
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page.startswith("Monitoring"):
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
