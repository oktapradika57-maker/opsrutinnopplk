import streamlit as st

st.set_page_config(page_title="Dashboard KUT", layout="wide")

# --- CSS PRESISI ---
st.markdown("""
    <style>
    /* Mengunci ukuran tombol agar kotak selalu besar dan sama persis */
    div.stButton > button {
        width: 100% !important;
        height: 250px !important;
        border-radius: 20px !important;
        border: 2px solid #444 !important;
        background: #262730 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: 0.3s !important;
    }
    
    /* Hover effect */
    div.stButton > button:hover {
        border-color: #6c63ff !important;
        background: #31333F !important;
        transform: scale(1.02);
    }
    
    /* Mengatur jarak kolom agar grid rapi */
    [data-testid="column"] {
        padding: 10px;
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
    
    # List menu (Icon + Nama)
    menus = [
        ("💰", "VARCOST"),
        ("🎯", "KPI"),
        ("🔧", "MAINTENANCE"),
        ("🏢", "ASSET"),
        ("🚀", "PROJECT"),
        ("⚙️", "OPERATIONAL")
    ]
    
    # Grid 3 kolom
    cols = st.columns(3)
    
    for i, (icon, label) in enumerate(menus):
        # Tombol langsung menggunakan teks ikon + label
        if cols[i % 3].button(f"{icon}\n\n{label}", key=label):
            navigate_to(f"Monitoring {label.capitalize()}")
    
elif st.session_state.current_page.startswith("Monitoring"):
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali ke Dashboard"): navigate_to("Halaman Depan")
    st.markdown("---")
    st.write(f"Konten untuk {st.session_state.current_page} sedang dimuat.")
