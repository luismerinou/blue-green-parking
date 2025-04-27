import streamlit as st

def render_main_title():
    """Configura el encabezado de la página HTML"""
    st.set_page_config(
        page_title="Blue green parking", page_icon=":blue_car:", layout="wide"
    )
    st.title("")
    st.markdown("""
        <h1 style='text-align: center; font-size:2.5rem; font-weight:700;'>Aparcamientos Zona SER Madrid</h1>
        <p style='text-align: center; color:#A1A1AA;'>Encuentra los aparcamientos más cercanos a ti o a tu destino</p>
    """, unsafe_allow_html=True)
