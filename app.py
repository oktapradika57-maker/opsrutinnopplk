import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# --- CSS PRESISI MUTLAK ---
st.markdown("""
    <style>
    /* 1. Memaksa grid agar setiap kolom sama rata */
    .menu-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        width: 100%;
    }
    
    /* 2. Mengunci ukuran tombol agar seragam di semua kondisi */
    div.stButton > button {
        width: 100% !important;
        height: 180px !important; 
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
    }
    
    /* 3. Efek hover agar lebih interaktif */
    div.stButton > button:hover {
        border-color: #6c63ff !important;
        background-color: #31333F !important;
        transform: translateY(-5px);
    }
    
    /* 4. Pengaturan ikon */
    .btn-icon { font-size: 40px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if 'current_page' not in st.session_state: st.session_state.current_page = "Halaman Depan"

if st.session_state.current_page == "Halaman Depan":
    st.title("✨ Dashboard Kinarya Utama Teknik")
    st.markdown("---")
    
    # Data Menu
    menus = [
        ("💰", "Varcost", "Monitoring Varcost"),
        ("🎯", "KPI", "Monitoring KPI"),
        ("🔧", "Maintenance", "Monitoring Preventive Maintenance"),
        ("🏢", "Asset", "Monitoring Asset"),
        ("🚀", "Project", "Monitoring Project"),
        ("⚙️", "Operational", "Monitoring Operational")
    ]
    
    # Memulai grid layout
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    
    # Looping tombol
    for icon, label, target in menus:
        # Menggunakan st.button biasa dengan label yang rapi agar tidak error sintaks
        # Streamlit akan merender teks ini dengan aman
        if st.button(f"{icon}\n{label}", key=label):
            navigate_to(target)
            
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "Monitoring Asset":
    st.title("🏢 Monitoring Asset")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    tab1, tab2 = st.tabs(["📦 Asset KUT", "🏗️ Asset Rental"])
    with tab1: st.write("Data Asset KUT...")
    with tab2: st.write("Data Asset Rental...")
else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
    st.write(f"Konten halaman {st.session_state.current_page} sedang diproses.")
