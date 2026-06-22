import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# --- CSS CUSTOM CARD DESIGN ---
st.markdown("""
    <style>
    .card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: 0.4s;
        cursor: pointer;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }
    .card img {
        width: 100px;
        height: 100px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    .card-title {
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
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
    
    # Data Menu
    menus = [
        ("Varcost", "Monitoring Varcost", "https://cdn-icons-png.flaticon.com/128/3135/3135706.png"),
        ("KPI", "Monitoring KPI", "https://cdn-icons-png.flaticon.com/128/2921/2921226.png"),
        ("Maintenance", "Monitoring Preventive Maintenance", "https://cdn-icons-png.flaticon.com/128/2942/2942813.png"),
        ("Asset", "Monitoring Asset", "https://cdn-icons-png.flaticon.com/128/2830/2830284.png"),
        ("Project", "Monitoring Project", "https://cdn-icons-png.flaticon.com/128/3063/3063198.png"),
        ("Operational", "Monitoring Operational", "https://cdn-icons-png.flaticon.com/128/2920/2920365.png")
    ]
    
    # Membuat Layout 3 Kolom
    cols = st.columns(3)
    for i, (title, target, img) in enumerate(menus):
        with cols[i % 3]:
            # Menggunakan st.container sebagai "Tombol"
            if st.container():
                st.markdown(f"""
                    <div class="card" onclick="window.location.href='?page={target}'">
                        <img src="{img}">
                        <div class="card-title">{title}</div>
                    </div>
                """, unsafe_allow_html=True)
                # Tombol transparan di atas card agar bisa diklik
                if st.button(f"Masuk {title}", key=title):
                    navigate_to(target)
    
else:
    st.title(f"📊 {st.session_state.current_page}")
    if st.button("⬅ Kembali"): navigate_to("Halaman Depan")
