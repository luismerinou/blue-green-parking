import streamlit as st
import pandas as pd
from pyproj import Transformer
import leafmap.foliumap as leafmap
import folium

df = pd.read_csv(
    'csv/ser_calles_mockfile.csv',
    delimiter=";",
    converters={
        'gis_x': lambda x: float(x.replace(',', '.')),
        'gis_y': lambda x: float(x.replace(',', '.'))
    },
    encoding='latin'
)

print(df)

gisx1 = df['gis_x'].iloc[0]
gisy1 = df['gis_y'].iloc[0]

gisx2 = df['gis_x'].iloc[7]
gisy2 = df['gis_y'].iloc[7]

print(f"gisx1:{type(gisx1)} gisx2:{type(gisx2)}")

transformer = Transformer.from_crs("epsg:25830", "epsg:4326", always_xy=True)

# Convertir coordenadas UTM a geográficas (latitud y longitud)
lon1, lat1 = transformer.transform(gisx1, gisy1)
lon2, lat2 = transformer.transform(gisx2, gisy2)

print(f"lat y longitud 1: {lon1}, {lat1}")
print(f"lat y longitud 2: {lon2}, {lat2}")
print()
leafmap_map = leafmap.Map(center=((lat1 + lat2) / 2, (lon1 + lon2) / 2), zoom=15)

# Añadir marcadores para los puntos
leafmap_map.add_marker(location=(lat1, lon1), popup="IR ")
leafmap_map.add_marker(location=(lat2, lon2), popup="Punto 2")

# Usar folium para agregar una línea entre los puntos
#line = folium.PolyLine(locations=[[lat1, lon1], [lat2, lon2]], color="red", weight=2)
#leafmap_map.add_layer(line)

# Mostrar el mapa en tamaño completo
leafmap_map.to_streamlit(height=1000, use_container_width=True)