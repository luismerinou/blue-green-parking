import streamlit as st
import folium
from streamlit_folium import st_folium

# Definir las coordenadas de los puntos
point1 = (40.414072, -3.721225)
point2 = (40.407945, -3.741631)
# point1 = (40.416775, -3.703790)  # Madrid
# point2 = (40.418056, -3.703889)  # Cerca de Madrid

# Crear un mapa de Folium centrado entre los dos puntos
m = folium.Map(location=[(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], zoom_start=15,
               tiles='CartoDB Voyager')

# Añadir marcadores para los puntos
folium.Marker(point1, popup="Punto 1").add_to(m)
folium.Marker(point2, popup="Punto 2").add_to(m)

# Añadir línea entre los puntos
folium.PolyLine(locations=[point1, point2], color="red").add_to(m)

# Mostrar el mapa en Streamlit
st_folium(m, width=700, height=500)

# Añadir un botón que genere la ruta en Google Maps
if st.button('Generar ruta en Google Maps'):
    lat1, lon1 = point1
    lat2, lon2 = point2
    url = f"https://www.google.com/maps/dir/{lat1},{lon1}/{lat2},{lon2}/&travelmode=walking"
    st.markdown(f"[Ver ruta en Google Maps]({url})")

if st.button("jola"):
    url="https://www.google.com/maps/dir/40.416775,-3.703790/40.418056,-3.703889/&travelmode=walking"
    st.markdown(f"[Ver ruta en Google Maps]({url})")




