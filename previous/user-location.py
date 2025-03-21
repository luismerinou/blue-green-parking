import streamlit as st
from streamlit_folium import st_folium
import folium
import leafmap.foliumap as leafmap
import json

get_location_js = """
<script>
function requestLocation() {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const coords = {
                lat: position.coords.latitude,
                lon: position.coords.longitude
            };
            localStorage.setItem('user_location', JSON.stringify(coords));
            document.dispatchEvent(new Event('locationUpdated'));
        },
        (error) => {
            console.error('Error obteniendo la ubicación:', error);
        }
    );
}

// Revocar permisos para que vuelva a solicitar ubicación
navigator.permissions.query({ name: 'geolocation' }).then((result) => {
    if (result.state !== 'prompt') {
        requestLocation();
    }
});
</script>
"""

st.components.v1.html(get_location_js, height=0)

if "user_lat" not in st.session_state or "user_lon" not in st.session_state:
    st.write(f"st.session_state[user_lat]: {st.session_state["user_lat"]}")
    st.write(f"st.session_state[user_lon]: {st.session_state["user_lon"]}")
    st.session_state["user_lat"] = 0
    st.session_state["user_lon"] = 0

lat1 = st.session_state["user_lat"]
lon1 = st.session_state["user_lon"]

if st.button("Obtener mi ubicación"):
    location_data = st.text_input("Pega aquí los datos de localStorage (lat, lon):")
    if location_data:
        st.write("location data")
        try:
            coords = json.loads(location_data)
            st.session_state["user_lat"] = coords["lat"]
            st.session_state["user_lon"] = coords["lon"]
            lat1, lon1 = coords["lat"], coords["lon"]
        except:
            st.error("Formato inválido. Inténtalo de nuevo.")

st.write(f"Coordenadas obtenidas: Latitud: {lat1}, Longitud: {lon1}")

if lat1 != 0 and lon1 != 0:
    leafmap_map = leafmap.Map(center=(lat1, lon1), zoom=15)
    leafmap_map.add_marker(location=(lat1, lon1), popup="Tu ubicación")
    leafmap_map.to_streamlit(height=700, use_container_width=True)
else:
    st.warning("Esperando ubicación... Pulsa el botón y sigue las instrucciones.")
