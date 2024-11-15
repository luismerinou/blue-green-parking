import streamlit as st
import pandas as pd
from pyproj import Transformer
import leafmap.foliumap as leafmap
import folium

st.set_page_config(layout="wide")

# Definir las coordenadas UTM (GISX y GISY)
gisx1, gisy1 = 439592.91, 4473566  # Punto 1
gisx2, gisy2 = 439600.00, 4473570  # Punto 2

# Definir el transformador
transformer = Transformer.from_crs("epsg:25830", "epsg:4326", always_xy=True)

# Convertir coordenadas UTM a geográficas (latitud y longitud)
lon1, lat1 = transformer.transform(gisx1, gisy1)
lon2, lat2 = transformer.transform(gisx2, gisy2)

# Mostrar las coordenadas convertidas
st.write(f"Coordenadas 1: Latitud: {lat1}, Longitud: {lon1}")
st.write(f"Coordenadas 2: Latitud: {lat2}, Longitud: {lon2}")

# Crear un mapa de Leafmap
m = leafmap.Map(center=((lat1 + lat2) / 2, (lon1 + lon2) / 2), zoom=15)

# Añadir marcadores para los puntos
m.add_marker(location=(lat1, lon1), popup="Punto 1")
m.add_marker(location=(lat2, lon2), popup="Punto 2")

# Usar folium para agregar una línea entre los puntos
line = folium.PolyLine(locations=[[lat1, lon1], [lat2, lon2]], color="red", weight=2)
m.add_layer(line)

# Mostrar el mapa en tamaño completo
m.to_streamlit(height=800, use_container_width=True)
