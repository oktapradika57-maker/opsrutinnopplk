import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        padding: 20px;
    }
    .card-3d {
        background: linear-gradient(145deg, #2d303e, #262730);
        height: 200px;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-decoration: none;
        color: white;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.1);
        /* Efek 3D */
        box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset 0 2px 2px rgba(255,255,255,0.1);
    }
    .card-3d:hover {
        transform: translateY(-15px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        border: 1px solid #6c63ff;
    }
    .icon-box { font-size: 50px; margin-bottom: 15px; }
    .label-box { font-size: 18px; font-weight: 700; letter-spacing: 1px; }
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
        ("💰", "Varcost", "Monitoring Varcost"),
        ("🎯", "KPI", "Monitoring KPI"),
        ("🔧", "Maintenance", "Monitoring Preventive Maintenance"),
        ("🏢", "Asset", "Monitoring Asset"),
        ("🚀", "Project", "Monitoring Project"),
        ("⚙️", "Operational", "Monitoring Operational")
    ]
    
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    for icon, label, target in menus:
        # Menggunakan st.button transparan di atas div 3D
        if st.button(f"{icon}\n{label}", key=label):
            navigate_to(target)
    st.markdown('</div>', unsafe_allow_html=True)

# ... sisa logika navigasi halaman sama seperti sebelumnya ...
