import streamlit as st

st.set_page_config(page_title="Corporate Dashboard", layout="wide")

# --- CSS PRESISI ---
st.markdown("""
    <style>
    /* 1. Menggunakan CSS Grid untuk memastikan grid 3 kolom yang sempurna */
    .grid-container {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 25px !important;
        padding: 10px !important;
    }
    
    /* 2. Memaksa tombol agar ukurannya tetap, tidak peduli isi teksnya */
    div.stButton > button {
        width: 100% !important;
        height: 200px !important; 
        border-radius: 20px !important;
        border: 2px solid #555 !important;
        background-color: #262730 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        /* Menggunakan flex agar ikon dan teks selalu di tengah */
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: 0.2s !important;
    }
    
    div.stButton > button:hover {
        border-color: #6c63ff !important;
        background-color: #31333
