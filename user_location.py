import logging
import sys

import streamlit as st
from dotenv import load_dotenv

from utils.map_utils import (
    init_session_state,
    get_location,
    geocode_location,
    get_location_suggestions
)
from utils.calculate_parking_lots import show_nearest_parking_lot_summary, show_nearby_parking_lots
from utils.device_utils import detect_device

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

st.set_page_config(
    page_title="Blue green parking", page_icon=":blue_car:", layout="wide"
)
# Apply Linear-like style
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background-color: #0E0E10;
            color: #FFFFFF;
        }
        .block-container {
            padding-top: 1rem !important;
        }
        .main {
            padding-top: 0rem !important;
        }
        .folium-map {
            border-radius: 12px;
            box-shadow: 0 0 25px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)


def search_bar(search_input, current_latitude, current_longitude):
    selected_place = None
    if search_input and len(search_input) >= 3:
        suggestions = get_location_suggestions(search_input)
        if suggestions:
            selected_place = st.selectbox("📍 Selecciona un destino", suggestions)

    if selected_place:
        dest_lat, dest_lon = geocode_location(selected_place)
        if dest_lat and dest_lon:
            st.success(f"Mostrando aparcamientos cercanos a: {selected_place}")
            return dest_lat, dest_lon
        else:
            st.error("No se pudo encontrar esa ubicación.")
            return current_latitude, current_longitude
    else:
        return current_latitude, current_longitude

def main():
    detect_device()
    st.title("")
    init_session_state()
    current_latitude, current_longitude, accuracy = get_location(logger)
    is_mobile = st.session_state["is_mobile"]

    if is_mobile:
        st.markdown("""
            <h1 style='text-align: center; font-size:2.5rem; font-weight:700;'>Aparcamientos Zona SER Madrid</h1>
            <p style='text-align: center; color:#A1A1AA;'>Encuentra los aparcamientos más cercanos a ti o a tu destino</p>
        """, unsafe_allow_html=True)
        search_input = st.text_input("🔍 Buscar otra ubicación (opcional):", placeholder="Ej. Nuevos Ministerios...")
        latitude_to_use, longitude_to_use = search_bar(search_input, current_latitude, current_longitude)
        show_nearby_parking_lots(latitude_to_use, longitude_to_use, distance_from_me=1000)
        show_nearest_parking_lot_summary(latitude_to_use, longitude_to_use, distance_from_me=1000)
    else:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("""
                <h1 style='text-align: center; font-size:2.5rem; font-weight:700;'>Aparcamientos Zona SER Madrid</h1>
                <p style='text-align: center; color:#A1A1AA;'>Encuentra los aparcamientos más cercanos a ti o a tu destino</p>
            """, unsafe_allow_html=True)
            search_input = st.text_input("🔍 Buscar otra ubicación (opcional):", placeholder="Ej. Nuevos Ministerios...")
            latitude_to_use, longitude_to_use = search_bar(search_input, current_latitude, current_longitude)
            show_nearest_parking_lot_summary(latitude_to_use, longitude_to_use, distance_from_me=1000)
        with col2:
            show_nearby_parking_lots(latitude_to_use, longitude_to_use, distance_from_me=1000)


if __name__ == "__main__":
    main()
