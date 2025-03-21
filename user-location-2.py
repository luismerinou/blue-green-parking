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
            // Guardar coordenadas en localStorage
            localStorage.setItem('user_location', JSON.stringify(coords));
            // Enviar coordenadas a Streamlit
            const streamlitData = document.createElement('div');
            streamlitData.id = 'streamlit-coords';
            streamlitData.textContent = JSON.stringify(coords);
            document.body.appendChild(streamlitData);
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

if "user_lat" not in st.session_state:
    st.session_state["user_lat"] = 0
if "user_lon" not in st.session_state:
    st.session_state["user_lon"] = 0

coords_container = st.empty()
coords_json = st.text_input("Coordenadas (detectadas automáticamente, no modificar):", "{}")

if coords_json:
    try:
        coords = json.loads(coords_json)
        st.session_state["user_lat"] = coords.get("lat", 0)
        st.session_state["user_lon"] = coords.get("lon", 0)
    except:
        st.error("Error al leer las coordenadas.")

lat1 = st.session_state["user_lat"]
lon1 = st.session_state["user_lon"]

st.write(f"Coordenadas obtenidas: Latitud: {lat1}, Longitud: {lon1}")

if lat1 != 0 and lon1 != 0:
    leafmap_map = leafmap.Map(center=(lat1, lon1), zoom=15)
    leafmap_map.add_marker(location=(lat1, lon1), popup="Tu ubicación")
    leafmap_map.to_streamlit(height=700, use_container_width=True)
else:
    st.warning("Esperando ubicación... Asegúrate de permitir el acceso a la geolocalización.")
