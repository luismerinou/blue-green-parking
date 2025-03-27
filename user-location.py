import streamlit as st
import logging
import sys
import folium
from streamlit_folium import st_folium
from streamlit_current_location import current_position

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
MADRID_SOL = {'lat': 40.416609, 'lon': -3.702556}


def create_map(latitude, longitude, zoom_start=15):
    mapa = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)
    folium.Marker([latitude, longitude], popup="¡Aquí estás!").add_to(mapa)
    return mapa


def get_location():
    location = current_position()
    st.write(
        f"""your location is 
        latitude: {location['latitude']}
        longitude: {location['longitude']}
        """
    )
    latitude = location["latitude"]
    longitude = location["longitude"]
    accuracy = 100

    if latitude is None or longitude is None:
        latitude, longitude = st.session_state.get("latitude"), st.session_state.get("longitude") # Puerta del Sol, Madrid

    return latitude, longitude, accuracy


def render_map(mapa):
    map_key = f"mapa_{st.session_state['latitude']}_{st.session_state['longitude']}"
    st_folium(mapa, width=700, height=500, key=map_key)


def init_session_state():
    if "map_initialized" not in st.session_state:
        st.session_state["map_initialized"] = False
        st.session_state["latitude"] = MADRID_SOL.get("lat")
        st.session_state["longitude"] = MADRID_SOL.get("lon")


def main():
    init_session_state()

    lat, long, accuracy = get_location()

    logger.info(f"Ubicación obtenida: Latitud: {lat}, Longitud: {long}")

    st.write(f"Ubicación obtenida: Latitud: {lat}, Longitud: {long}, Accuracy: {accuracy}")

    mapa = create_map(lat, long)
    render_map(mapa)


if __name__ == '__main__':
    main()
