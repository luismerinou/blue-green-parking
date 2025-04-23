import logging
import sys

import folium
import streamlit as st

from utils.icons_utils import get_car_side_icon, get_pop_up_content
from utils.map_utils import (
    create_map,
    render_map
)
from utils.sql_utils import get_parking_lots_around_me, get_nearest_parking_lot_from_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

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

@st.cache_data
def get_cached_nearest_parking_lots_from_user(latitude, longitude, distance_from_me):
    """Gets all user nearest parking lots"""
    logger.info("Ejecutando búsqueda de aparcamientos en caché...")
    mapa = create_map(latitude, longitude, add_marker=True)

    nearest_user_parking_lot = get_nearest_parking_lot_from_user(
        logger,
        distance_from_me=distance_from_me,
        current_longitude=longitude,
        current_latitude=latitude,
    )

    return nearest_user_parking_lot

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

def show_nearest_parking_lot_summary(latitude, longitude, distance_from_me=1000):
    """Gets the user's nearest parking lot"""
    nearest_parking = get_cached_nearest_parking_lots_from_user(
        latitude, longitude, distance_from_me
    )

    if not nearest_parking:
        st.warning("No se encontró ningún aparcamiento cercano.")
        return
    (
        longitud,
        latitud,
        barrio,
        calle,
        color,
        bateria_linea,
        num_plazas,
        distancia_metros,
    ) = nearest_parking[0]

    directions_url = f"https://www.google.com/maps/dir/?api=1&origin={latitude},{longitude}&destination={latitud},{longitud}"

    st.markdown(f"""
    <div style="background-color:#1E1E1E; padding: 1rem; border-radius: 12px; margin-top: 1rem;">
        <h3 style="margin-bottom: 0.5rem;">🅿️ Aparcamiento más cercano</h3>
        <p>Tu aparcamiento más cercano está a <strong>{round(distancia_metros, 0)}m</strong>, con <strong>{num_plazas}</strong> plazas en zona <strong style="color:{'blue' if color.lower() == 'azul' else 'green'};">{color}</strong>.</p>
        <a href="{directions_url}" target="_blank" style="display:inline-block; background-color:#2563EB; color:white; padding:0.5rem 1rem; border-radius:8px; text-decoration:none; font-weight:600;">Ver en Google Maps</a>
    </div>
    """, unsafe_allow_html=True)

