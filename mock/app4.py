import streamlit as st
import pandas as pd
from pyproj import Transformer
import folium

# Subir el archivo CSV
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])


def load_csv(file):
    try:
        # Intentamos con la codificación 'utf-8-sig' para manejar caracteres especiales
        df = pd.read_csv(file, delimiter=';', encoding='utf-8-sig', header=0)
    except UnicodeDecodeError:
        try:
            # Si falla, intentamos con 'latin1', que también es común para CSVs en español
            df = pd.read_csv(file, delimiter=';', encoding='latin1', header=0)
        except UnicodeDecodeError:
            # Intentamos con 'cp1252' si las anteriores no funcionan
            df = pd.read_csv(file, delimiter=';', encoding='cp1252', header=0)
    return df


if uploaded_file is not None:
    # Cargar el CSV
    df = load_csv(uploaded_file)

    # Mostrar las primeras filas del DataFrame para verificar el contenido
    st.write("Datos cargados:")
    st.write(df.head())

    # Mostrar los nombres de las columnas para depurar el problema
    st.write("Nombres de las columnas:", df.columns)

    # Verificar si las columnas necesarias existen en el CSV
    if 'gis_x' in df.columns and 'gis_y' in df.columns:

        # Definir el transformador de UTM a geográficas (usando EPSG:25830 para UTM y EPSG:4326 para lat/lon)
        transformer = Transformer.from_crs("epsg:25830", "epsg:4326", always_xy=True)

        # Crear nuevas columnas con las coordenadas geográficas
        df['lat'], df['lon'] = zip(*df.apply(lambda row: transformer.transform(row['gis_x'], row['gis_y']), axis=1))

        # Mostrar las primeras filas con las coordenadas convertidas
        st.write("Datos con coordenadas geográficas:", df[['gis_x', 'gis_y', 'lat', 'lon']].head())

        # Crear un mapa centrado en el promedio de las coordenadas
        map_center = [df['lat'].mean(), df['lon'].mean()]
        m = folium.Map(location=map_center, zoom_start=12)

        # Añadir los puntos como marcadores
        for i, row in df.iterrows():
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f"{row['barrio']} - {row['calle']} {row['num_finca']}",  # Información del popup
            ).add_to(m)

        # Mostrar el mapa en Streamlit
        st.write(m._repr_html_(), unsafe_allow_html=True)

    else:
        st.error("El archivo CSV debe contener las columnas 'gis_x' y 'gis_y' para las coordenadas.")
