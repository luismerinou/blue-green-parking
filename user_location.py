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

import streamlit as st


@st.cache_data
def get_cached_parking_lots(latitude, longitude, distance_from_me):
    logger.info("Ejecutando búsqueda de aparcamientos en caché...")

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
                distrito,
                barrio,
                calle,
                num_finca,
                color,
                bateria_linea,
                num_plazas,
                gis_x,
                gis_y,
                longitud,
                latitud,
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
                icon=get_car_side_icon(),
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
    st.title("Blue green parking")
    init_session_state()
    try:
        current_latitude, current_longitude, accuracy = get_location(logger)
        # current_latitude, current_longitude, accuracy = (
        #     MADRID_SOL.get("lat"),
        #     MADRID_SOL.get("lon"),
        #     0,
        # )

        st.write(
            f"Ubicación obtenida: Latitud: {current_latitude}, Longitud: {current_longitude}, Accuracy: {accuracy}"
        )

        show_nearby_parking_lots(
            current_latitude, current_longitude, distance_from_me=1000
        )

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
