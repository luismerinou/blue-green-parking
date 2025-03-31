import folium
import streamlit as st
from streamlit_current_location import current_position
from streamlit_folium import st_folium

from custom_exceptions.LocationError import LocationError
from utils.icons_utils import get_my_location_icon

MADRID_SOL = {"lat": 40.416609, "lon": -3.702556}


def create_map(latitude, longitude, zoom_start=15, add_marker=False):
    mapa = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)
    if add_marker:
        folium.Marker([latitude, longitude], popup="¡Aquí estás!", icon=get_my_location_icon()).add_to(mapa)
    return mapa


def render_map(mapa):
    map_key = f"mapa_{st.session_state['latitude']}_{st.session_state['longitude']}"
    st_folium(mapa, width=2000, height=520, key=map_key)


def init_session_state():
    if "map_initialized" not in st.session_state:
        st.session_state["map_initialized"] = False
        st.session_state["latitude"] = MADRID_SOL.get("lat")
        st.session_state["longitude"] = MADRID_SOL.get("lon")


def get_location(logger):
    location = current_position()
    if not location:
        logger.warning(
            "Current location not found, displaying default location MADRID PUERTA DEL SOL"
        )
        return MADRID_SOL.get("lat"), MADRID_SOL.get("lon"), 100
    else:
        st.write(
            f"""Tu ubicación es 
            Latitud: {location.get("latitude", "N/A")}
            Longitud: {location.get("longitude", "N/A")}
            """
        )
        latitude = location.get("latitude", "N/A")
        longitude = location.get("longitude", "N/A")
        accuracy = 100

        if None in (latitude, longitude, accuracy):
            raise LocationError("Faltan datos de ubicación.", location_data=location)
        else:
            logger.info(
                f"Ubicación obtenida: Latitud: {latitude}, Longitud: {longitude}, Accuracy: {accuracy}"
            )
            return latitude, longitude, accuracy
