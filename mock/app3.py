import streamlit as st
import pandas as pd
from pyproj import Transformer
import folium

# Subir archivo CSV
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Leer el CSV en un DataFrame
    df = pd.read_csv(uploaded_file, delimiter=";", encoding='latin1')

    # Mostrar las primeras filas del DataFrame para verificar el contenido
    st.write("Datos cargados:", df.head())
    st.write("Nombres de las columnas:", df.columns)

    # Verificar si el CSV tiene las columnas necesarias (gis_x y gis_y)
    if 'gis_x' in df.columns and 'gis_y' in df.columns:

        # Convertir las columnas 'gis_x' y 'gis_y' a numéricas, invalidos serán convertidos a NaN
        df['gis_x'] = pd.to_numeric(df['gis_x'], errors='coerce')
        df['gis_y'] = pd.to_numeric(df['gis_y'], errors='coerce')

        # Limpiar los valores no válidos (NaN) eliminando las filas
        df_clean = df.dropna(subset=['gis_x', 'gis_y'])

        # Opción alternativa: Reemplazar los valores NaN con un valor por defecto (ejemplo: 0)
        df['gis_x'].fillna(0, inplace=True)
        df['gis_y'].fillna(0, inplace=True)

        # Verificar si hay valores nulos después de la limpieza
        if df_clean[['gis_x', 'gis_y']].isnull().any().any():
            st.error("Todavía hay valores nulos en las coordenadas.")
        else:
            # Definir el transformador de UTM a geográficas (usando EPSG:25830 para UTM y EPSG:4326 para lat/lon)
            transformer = Transformer.from_crs("epsg:25830", "epsg:4326", always_xy=True)

            # Crear nuevas columnas con las coordenadas geográficas
            df_clean['lat'], df_clean['lon'] = transformer.transform(df_clean['gis_x'].values, df_clean['gis_y'].values)

            # Mostrar las primeras filas con las coordenadas convertidas
            st.write("Datos con coordenadas geográficas:", df_clean[['gis_x', 'gis_y', 'lat', 'lon']].head())

            # Crear un mapa centrado en el promedio de las coordenadas
            map_center = [df_clean['lat'].mean(), df_clean['lon'].mean()]
            m = folium.Map(location=map_center, zoom_start=12)

            # Añadir los puntos como marcadores
            for i, row in df_clean.iterrows():
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=f"{row['barrio']} - {row['calle']} {row['num_finca']}",  # Información del popup
                ).add_to(m)

            # Mostrar el mapa en Streamlit
            st.write(m._repr_html_(), unsafe_allow_html=True)

            # Mostrar el mapa en Streamlit
            m.to_streamlit(height=500)

    else:
        st.error("El archivo CSV debe contener las columnas 'gis_x' y 'gis_y' para las coordenadas.")
