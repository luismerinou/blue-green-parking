import streamlit as st
import pandas as pd
import folium
from io import StringIO
import pyproj
from streamlit_folium import st_folium

# Crear un objeto pyproj para la proyección UTM (suponiendo que las coordenadas están en UTM 30N)
utm_proj = pyproj.Proj(proj="utm", zone=30, datum="WGS84")
lat_lon_proj = pyproj.Proj(proj="latlong", datum="WGS84")

# Función para convertir coordenadas UTM (gis_x, gis_y) a lat, lon
def convert_utm_to_latlon(x, y):
    lon, lat = pyproj.transform(utm_proj, lat_lon_proj, x, y)
    return lat, lon

# Ejemplo de datos CSV con coordenadas GIS (UTM)
DATA = """
gis_x;gis_y;distrito;barrio;calle;num_finca;color;bateria_linea;num_plazas
439592.91;4473566.23;01  CENTRO;01-01 PALACIO;AGUAS, CALLE, DE LAS;2;Verde;Línea;7
439569.07;4473598.77;01  CENTRO;01-01 PALACIO;AGUAS, CALLE, DE LAS;8;Verde;Línea;5
439578.18;4473498.76;01  CENTRO;01-01 PALACIO;AGUILA, CALLE, DEL;3;Verde;Línea;1
439574.49;4473493.4;01  CENTRO;01-01 PALACIO;AGUILA, CALLE, DEL;5;Verde;Línea;1
"""

# Cargar los datos del CSV
data = pd.read_csv(StringIO(DATA), sep=';')

# Convertir las coordenadas UTM a latitud y longitud
data['lat'], data['lon'] = zip(*data.apply(lambda row: convert_utm_to_latlon(row['gis_x'], row['gis_y']), axis=1))

# Crear el mapa con Folium, centrado en una ubicación inicial (por ejemplo, el primer punto de datos)
m = folium.Map(location=[data['lat'][0], data['lon'][0]], zoom_start=13)

# Añadir los puntos al mapa con marcadores
for _, row in data.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"{row['barrio']}, {row['calle']} - {row['num_plazas']} plazas"
    ).add_to(m)

# Visualizar el mapa usando Streamlit y Folium
st.title("Mapa de Plazas de Aparcamiento")
st_folium(m, width=700, height=500)
