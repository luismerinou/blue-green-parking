import streamlit as st
import pandas as pd
from pyproj import Transformer
import folium
import logging
from streamlit.components.v1 import html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función para cargar el archivo CSV
def load_csv(file_name: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(
            file_name,
            delimiter=";",
            converters={
                'gis_x': lambda x: float(x.replace(',', '.')),
                'gis_y': lambda x: float(x.replace(',', '.'))
            },
            encoding='latin'
        )
        logger.info(f"CSV '{file_name}' cargado exitosamente.")
        return df
    except Exception as e:
        logger.error(f"Error al cargar el CSV: {e}")
        st.error(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()

# Función para agregar puntos al mapa
def add_points_to_map(dataframe: pd.DataFrame, map_object: folium.Map):
    if dataframe.empty:
        st.warning("El DataFrame está vacío. No se pueden agregar puntos.")
        return

    transformer = Transformer.from_crs("epsg:25830", "epsg:4326", always_xy=True)

    for index, row in dataframe.iterrows():
        try:
            gis_x = row.get('gis_x', "N/A")
            gis_y = row.get('gis_y', "N/A")

            if pd.notnull(gis_x) and pd.notnull(gis_y):
                longitude, latitude = transformer.transform(gis_x, gis_y)
                numero_plazas = dataframe.get('num_plazas').iloc[index]
                nombre_de_calle = dataframe.get('calle').iloc[index]
                numero_calle = dataframe.get('num_finca').iloc[index]
                barrio = dataframe.get('barrio').iloc[index][-7:]
                distrito = dataframe.get('distrito').iloc[index][-6:]
                distrito_col = dataframe.columns[2]
                barrio_col = dataframe.columns[3]
                nombre_calle_col = dataframe.columns[4]
                num_plaza_col = dataframe.columns[8]
                color_plaza = dataframe.get('color').iloc[index][10:]

                # HTML y estilo del popup
                popup_html = f"""
                    <style>
                        .custom-popup {{
                            background-color: #f0f0f0;
                            color: #333;
                            font-family: Arial, sans-serif;
                            padding: 30px;  /* Aumenta el padding para más espacio */
                            border-radius: 12px;  /* Bordes redondeados */
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);  /* Sombra más fuerte */
                            max-width: 500px;  /* Aumenta el tamaño máximo del popup */
                            font-size: 5px;  /* Aumenta el tamaño de la fuente */
                        }}
                        .custom-popup h4 {{
                            font-size: 18px;
                            color: #1a1a1a;
                            margin-bottom: 12px;  /* Separación entre los títulos */
                        }}
                        .custom-popup p {{
                            font-size: 14px;
                            color: #555;
                        }}
                    </style>
                    <div class="custom-popup">
                        <h4>{distrito_col}: {distrito}</h4>
                        <h4>{barrio_col}: {barrio}</h4>
                        <h4>{nombre_calle_col}: {nombre_de_calle}. nº {numero_calle}</h4>
                        <h4>{num_plaza_col}: {numero_plazas}</h4>
                    </div>
                """

                # Mapa de colores
                color_map = {
                    'Verde': 'green',
                    'Azul': 'blue',
                }

                icon_html = f"""
                        <div style="position: relative; text-align: center; font-size: 18px;">
                            <div style="background-color: {color_map.get(color_plaza, 'gray')}; 
                                        width: 40px; 
                                        height: 40px; 
                                        border-radius: 50%; 
                                        color: white; 
                                        line-height: 40px; 
                                        font-weight: bold; 
                                        margin-bottom: -20px;">
                                {numero_plazas}
                            </div>
                            <div style="position: absolute; top: 32px; left: 50%; transform: translateX(-50%); 
                                        width: 0; height: 0; border-left: 10px solid transparent; 
                                        border-right: 10px solid transparent; 
                                        border-top: 15px solid {color_plaza};"></div>
                        </div>
                    """

                icon_div = folium.DivIcon(html=icon_html)
                folium.Marker(
                    location=(latitude, longitude),
                    popup=popup_html,
                    icon=icon_div
                ).add_to(map_object)
                map_object.add_child(folium.LatLngPopup())  # Muestra las coordenadas al hacer click
            else:
                logger.warning(f"Coordenadas inválidas en la fila: {row}")
        except Exception as e:
            logger.error(f"Error al procesar la fila: {e}")

    # Usamos `folium` con `streamlit.components.v1.html` para mostrar el mapa en Streamlit
    map_html = map_object._repr_html_()
    html(map_html, height=800)

# Función principal
def main():
    st.set_page_config(layout="wide", page_title="Mapa Interactivo", page_icon="🌍")

    st.title("Visualización de Puntos en un Mapa")

    with st.spinner("Cargando datos..."):
        uploaded_file = 'csv/ser_calles_mockfile.csv'
        df = load_csv(uploaded_file)

    if not df.empty:
        st.success("Datos cargados correctamente.")
        st.write("Vista previa de los datos:", df.head())

        st.subheader("Mapa Interactivo")
        map_object = folium.Map(location=(40.417145, -3.703488), zoom_start=15)
        add_points_to_map(df, map_object)
    else:
        st.error("El archivo cargado no contiene datos válidos.")

# Ejecución
if __name__ == '__main__':
    main()
