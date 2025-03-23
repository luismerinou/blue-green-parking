import folium
import streamlit as st
from streamlit_folium import st_folium

# Crear un mapa centrado en un punto específico
m = folium.Map(location=[40.4168, -3.7038], zoom_start=12)  # Centrado en Madrid, España

# Definir las coordenadas del polígono (en latitud y longitud)
polygon_coords = [
    [40.4168, -3.7038],  # Punto A (Madrid)
    [40.4178, -3.7035],  # Punto B
    [40.4185, -3.7028],  # Punto C
    [40.4170, -3.7018],  # Punto D
    [40.4168, -3.7038]   # Punto A (cerramos el polígono)
]

# Estilo para el polígono (rojo y completamente opaco)
polygon_style = {
    'fillColor': 'red',  # Color de relleno rojo
    'color': 'red',      # Color de borde rojo
    'weight': 2,         # Grosor del borde
    'opacity': 0.1,        # Borde completamente opaco
    'fillOpacity': 0.1     # Relleno completamente opaco
}

# Crear el polígono en Folium
folium.Polygon(
    locations=polygon_coords,  # Coordenadas del polígono
    color='red',               # Borde rojo
    weight=2,                  # Grosor del borde
    fill=True,                 # Activar relleno
    fill_color='red',          # Color de relleno rojo
    fill_opacity=0.1             # Relleno completamente opaco
).add_to(m)

# Mostrar el mapa con el polígono en Streamlit
st.title("Polígono Opaco en Folium")
st_folium(m, width=700, height=500)
