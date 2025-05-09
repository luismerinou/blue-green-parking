import folium
import streamlit as st
from streamlit_current_location import current_position
from streamlit_folium import st_folium
import requests

from shared.exceptions.LocationError import LocationError
from shared.utils.Icon import get_my_location_icon

MADRID_SOL = {"lat": 40.416609, "lon": -3.702556}


@st.cache_data(ttl=600)
def get_location_suggestions(query):
    """Devuelve sugerencias de ubicación a partir de un texto de búsqueda."""
    if not query or len(query) < 3:
        return []

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 5,
    }

    response = requests.get(url, params=params, headers={"User-Agent": "blue-green-parking-app"})
    if response.status_code == 200:
        return [item["display_name"] for item in response.json()]
    return []

def geocode_location(location_name):
    """Convierte un nombre de ubicación en coordenadas de latitud y longitud."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1,
    }

    response = requests.get(url, params=params, headers={"User-Agent": "blue-green-parking-app"})
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        return float(result["lat"]), float(result["lon"])
    else:
        return None, None

def create_map(latitude, longitude, zoom_start=16, add_marker=False):
    """Crea un mapa de Folium centrado en las coordenadas especificadas."""
    if st.session_state.get("is_mobile", False):
        zoom_start = 15
    mapa = folium.Map(
        location=[latitude, longitude],
        zoom_start=zoom_start,
        tiles="CartoDB dark_matter"
    )
    if add_marker:
        folium.Marker(
            [latitude, longitude], popup="¡Aquí estás!", icon=get_my_location_icon()
        ).add_to(mapa)
    return mapa


def render_map(mapa):
    """Renderiza un mapa de Folium en Streamlit con altura adaptativa."""
    is_mobile = st.session_state.get("is_mobile", False)
    window_height = st.session_state.get("screen_height", 800)
    height = int(window_height * 0.8) if is_mobile else int(window_height * 0.85)

    map_key = f"mapa_{st.session_state['latitude']}_{st.session_state['longitude']}"
    st_folium(mapa, width="100%", height=height, key=map_key)


def init_session_state():
    """Inicializa el estado de sesión de Streamlit con una ubicación predeterminada."""
    if "map_initialized" not in st.session_state:
        st.session_state["map_initialized"] = False
        st.session_state["latitude"] = MADRID_SOL.get("lat")
        st.session_state["longitude"] = MADRID_SOL.get("lon")


def get_location(logger):
    """Obtiene la ubicación actual del usuario o una ubicación por defecto."""
    location = current_position()
    logger.info(location)
    if not location:
        logger.warning(
            "Current location not found, displaying default location MADRID PUERTA DEL SOL"
        )
        return MADRID_SOL.get("lat"), MADRID_SOL.get("lon")
    else:
        st.write(
            f"""Tu ubicación es 
            Latitud: {location.get("latitude", "N/A")}
            Longitud: {location.get("longitude", "N/A")}
            """
        )
        latitude = location.get("latitude", "N/A")
        longitude = location.get("longitude", "N/A")

        if None in (latitude, longitude):
            raise LocationError("Faltan datos de ubicación.", location_data=location)
        else:
            logger.info(
                f"Ubicación obtenida: Latitud: {latitude}, Longitud: {longitude}"
            )
            return latitude, longitude
