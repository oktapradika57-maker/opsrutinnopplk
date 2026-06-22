import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS PRESISI DENGAN GRID & ASPECT RATIO ---
st.markdown("""
    <style>
    /* Kontainer utama untuk landscape */
    .grid-layout {
        display: grid;
        grid-template-columns: repeat(6, 1fr); /* 6 kolom sama rata */
        gap: 20px;
        margin-top: 20px;
    }
    
    /* Paksa tombol menjadi kotak sempurna (aspect-ratio) */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important; /* Membuat kotak selalu persegi/presisi */
        border-radius: 20px !important;
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
        transform: scale(1.05);
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
    
    menus = [
        ("💰", "VARCOST"), ("🎯", "KPI"), ("🔧", "MAINTENANCE"),
        ("🏢", "ASSET"), ("🚀", "PROJECT"), ("⚙️", "OPERATIONAL")
    ]
    
    # Render Landscape menggunakan grid CSS
    st.markdown('<div class="grid-layout">', unsafe_allow_html=True)
    
    # Kita buat tombol di setiap kolom
    for icon, label in menus:
        if st.button(f"{icon}\n\n{label}", key=label):
            navigate_to(f"Monitoring {label.capitalize()}")
            
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page.startswith("Monitoring"):
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Dashboard"): navigate_to("Halaman Depan")
