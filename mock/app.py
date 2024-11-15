import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
lat, lon = 40.416775, -3.703790
lat2, lon2 = 40.5635072, -3.9256064
# Create a DataFrame with the points you want to highlight
data = pd.DataFrame({
    'latitude': [lat, lat2],
    'longitude': [lon, lon2]
})

# Add the highlight points to the map
st.map(data)


# Crear un objeto geolocalizador
geolocator = Nominatim(user_agent="myGeocoder")

# Obtener la dirección a partir de las coordenadas
location1 = geolocator.reverse((lat, lon), exactly_one=True)
location2 = geolocator.reverse((lat2, lon2), exactly_one=True)

# Mostrar la dirección
st.write(location1.address)
st.write(location2.address)
