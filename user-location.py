import streamlit as st
import logging
import sys
import folium
from streamlit_folium import st_folium
from streamlit_current_location import current_position

from custom_exceptions.LocationError import LocationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
MADRID_SOL = {'lat': 40.416609, 'lon': -3.702556}


def create_map(latitude, longitude, zoom_start=15, add_marker=False):
    mapa = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)
    if add_marker:
        folium.Marker([latitude, longitude], popup="¡Aquí estás!").add_to(mapa)
    return mapa


def render_map(mapa):
    map_key = f"mapa_{st.session_state['latitude']}_{st.session_state['longitude']}"
    st_folium(mapa, width=700, height=500, key=map_key)


def init_session_state():
    if "map_initialized" not in st.session_state:
        st.session_state["map_initialized"] = False
        st.session_state["latitude"] = MADRID_SOL.get("lat")
        st.session_state["longitude"] = MADRID_SOL.get("lon")


def get_location():
    location = current_position()
    if not location:
        return MADRID_SOL.get('lat'), MADRID_SOL.get('lon'), 100
    else:
        st.write(
            f"""Tu ubicación es 
            Latitud: {location.get('latitude', 'N/A')}
            Longitud: {location.get('longitude', 'N/A')}
            """
        )
        latitude = location.get('latitude', 'N/A')
        longitude = location.get('longitude', 'N/A')
        accuracy = 100

        if None in (latitude, longitude, accuracy):
            raise LocationError(
                "Faltan datos de ubicación.",
                location_data=location
            )
        else:
            logger.info(f"Ubicación obtenida: Latitud: {latitude}, Longitud: {longitude}, Accuracy: {accuracy}")
            return latitude, longitude, accuracy


def main():
    init_session_state()
    try:
        lat, long, accuracy = get_location()

        st.write(f"Ubicación obtenida: Latitud: {lat}, Longitud: {long}, Accuracy: {accuracy}")

        mapa = create_map(lat, long, add_marker=True)
        render_map(mapa)

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()
