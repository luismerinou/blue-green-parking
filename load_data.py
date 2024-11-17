import sys

import streamlit as st
import pandas as pd
from pandas import DataFrame
from pyproj import Transformer
from pyproj import Transformer
import leafmap.foliumap as leafmap
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# import folium
# # Usar folium para agregar una línea entre los puntos
# # line = folium.PolyLine(locations=[[lat1, lon1], [lat2, lon2]], color="red", weight=2)
# # leafmap_map.add_layer(line)
#

def load_csv(file_name: str) -> DataFrame:
    df = pd.read_csv(
        file_name,
        delimiter=";",
        converters={
            'gis_x': lambda x: float(x.replace(',', '.')),
            'gis_y': lambda x: float(x.replace(',', '.'))
        },
        encoding='latin'
    )
    logger.info(f"# CSV {file_name} loaded! #")
    print(df)

    return df


def add_points_to_map(dataframe: DataFrame, leafmap_map: leafmap.Map):
    transformer = Transformer.from_crs("epsg:25830", "epsg:4326", always_xy=True)

    for index, row in dataframe.iterrows():
        gisx1 = dataframe.get('gis_x').iloc[index]
        gisy1 = dataframe.get('gis_y').iloc[index]

        if pd.notnull(gisx1) and pd.notnull(gisy1):
            longitude, latitude = transformer.transform(gisx1, gisy1)
        else:
            logger.warning(f"Datos inválidos para la fila: {row}")
        # longitude, latitude = transformer.transform(gisx1, gisy1)
        logger.info(f"## Latitud y longitud [ {index} ]: {longitude}, {latitude}")
        popup_html = f"""
        <div>
            <h4>{dataframe.columns[2]}: {dataframe.get('distrito').iloc[index][-6:]}</h4>
            <h4>{dataframe.columns[3]}: {dataframe.get('barrio').iloc[index][-7:]}</h4>
            <h4>{dataframe.columns[4]}: {dataframe.get('calle').iloc[index]}. nº {dataframe.get('num_finca').iloc[index]}</h4>
            <h4>{dataframe.columns[8]}: {dataframe.get('num_plazas').iloc[index]}</h4>
        </div>
        """
        logger.info(f"## Distrito: /{dataframe.get('distrito').iloc[index][-6:]}/")

        leafmap_map.add_marker(location=(latitude, longitude), popup=popup_html)
    leafmap_map.to_streamlit(height=800, use_container_width=True)


def main():
    st.set_page_config(layout="wide")
    leafmap_map = leafmap.Map(center=(40.417145, -3.703488), zoom=15)  # puerta del sol
    df = load_csv('csv/ser_calles_mockfile.csv')
    logger.info(df.__sizeof__())
    add_points_to_map(df, leafmap_map)


if __name__ == '__main__':
    main()
