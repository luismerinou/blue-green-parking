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
    'opacity': 1,        # Borde completamente opaco
    'fillOpacity': 1     # Relleno completamente opaco
}

# Crear el polígono en Folium
polygon = folium.Polygon(
    locations=polygon_coords,  # Coordenadas del polígono
    color='red',               # Borde rojo
    weight=2,                  # Grosor del borde
    fill=True,                 # Activar relleno
    fill_color='red',          # Color de relleno rojo
    fill_opacity=1             # Relleno completamente opaco
).add_to(m)

# Función para obtener el centro del polígono y agregar un marcador
def add_marker_on_click(polygon):
    # Obtener los límites del polígono
    bounds = polygon.get_bounds()
    # Calcular el centro del polígono (promedio de las latitudes y longitudes)
    lat_center = (bounds[0][0] + bounds[1][0]) / 2
    lon_center = (bounds[0][1] + bounds[1][1]) / 2

    # Crear un marcador en el centro del polígono
    folium.Marker(
        location=[lat_center, lon_center],
        popup="Centro del polígono"
    ).add_to(m)

# Añadir evento de clic al polígono
polygon.add_child(folium.Popup("Haz clic en el polígono para mostrar el marcador en el centro"))
polygon.add_child(folium.LatLngPopup())  # Esto permite que el mapa muestre las coordenadas cuando se hace clic en él

# Hacer que al hacer clic en el polígono se agregue un marcador en el centro
polygon.add_child(folium.GeoJson(
    data={
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon_coords]
            }
        }]
    },
    on_click=lambda e: add_marker_on_click(polygon)
))

# Mostrar el mapa con el polígono en Streamlit
st.title("Polígono con Marcador en el Centro")
st_folium(m, width=700, height=500)
