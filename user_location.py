import logging
import sys

import folium
import streamlit as st
from dotenv import load_dotenv

from utils.icons_utils import get_car_side_icon, get_page_icon, get_pop_up_content
from utils.map_utils import (
    MADRID_SOL,
    create_map,
    render_map,
    init_session_state,
    get_location,
)
from utils.sql_utils import get_parking_lots_around_me
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

@st.cache_data
def get_cached_parking_lots(latitude, longitude, distance_from_me):
    logger.info("Ejecutando búsqueda de aparcamientos en caché...")
    mapa = create_map(latitude, longitude, add_marker=True)

    parking_lots_near_me = get_parking_lots_around_me(
        logger,
        distance_from_me=distance_from_me,
        current_longitude=longitude,
        current_latitude=latitude,
    )

    return parking_lots_near_me


def show_nearby_parking_lots(latitude, longitude, distance_from_me=500):
    mapa = create_map(latitude, longitude, zoom_start=15, add_marker=True)

    parking_lots_near_me = get_cached_parking_lots(latitude, longitude, distance_from_me)

    if parking_lots_near_me:
        total_lat = 0
        total_lon = 0
        marker_count = 0

        for parking in parking_lots_near_me:
            (
                longitud,
                latitud,
                barrio,
                calle,
                num_finca,
                color,
                bateria_linea,
                num_plazas,
                distancia_metros,
            ) = parking

            logger.info(f"Parking lot: {parking}")
            directions_url = f"https://www.google.com/maps/dir/?api=1&origin={latitude},{longitude}&destination={latitud},{longitud}"

            popup_content = get_pop_up_content(
                calle,
                num_finca,
                barrio,
                distancia_metros,
                num_plazas,
                bateria_linea,
                directions_url,
            )

            folium.Marker(
                location=[latitud, longitud],
                popup=folium.Popup(popup_content, max_width=300),
                icon=get_car_side_icon(color),
            ).add_to(mapa)

            total_lat += latitud
            total_lon += longitud
            marker_count += 1

        if marker_count > 0:
            avg_lat = total_lat / marker_count
            avg_lon = total_lon / marker_count
            mapa.location = [avg_lat, avg_lon]

        render_map(mapa)
    else:
        logger.info(
            f"No nearby blue parking lots found at {distance_from_me} m from your current location lat:{latitude}, lon:{longitude}"
        )
        st.write(
            f"No hay aparcamientos azules cercanos a {distance_from_me} metros de tu posición."
        )
        render_map(mapa)

def main():
    detect_device()
    st.title("")
    init_session_state()
    current_latitude, current_longitude, accuracy = get_location(logger)

    is_mobile = st.session_state["is_mobile"]

    if is_mobile:
        st.markdown("""
            <h1 style='text-align: center; font-size:2.5rem; font-weight:700;'>Aparcamientos Zona SER Madrid</h1>
            <p style='text-align: center; color:#A1A1AA;'>Encuentra los aparcamientos más cercanos a ti</p>
        """, unsafe_allow_html=True)
        show_nearby_parking_lots(current_latitude, current_longitude, distance_from_me=1000)

    else:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("""
                <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
                    <h1 style="font-size:3rem; font-weight:700; margin-bottom: 0.5rem;">Aparcamientos Zona SER Madrid</h1>
                    <p style="font-size:1.1rem; color:#A1A1AA;">Encuentra los aparcamientos más cercanos a ti</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            show_nearby_parking_lots(current_latitude, current_longitude, distance_from_me=1000)

if __name__ == "__main__":
    main()
