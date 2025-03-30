import logging
import os
import sys

import folium
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from streamlit_current_location import current_position
from streamlit_folium import st_folium

from custom_exceptions.LocationError import LocationError

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

MADRID_SOL = {'lat': 40.416609, 'lon': -3.702556}
DB_URL = os.environ.get("DB_URL")
# st.set_page_config(layout="wide")

def create_map(latitude, longitude, zoom_start=15, add_marker=False):
    mapa = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)
    if add_marker:
        folium.Marker([latitude, longitude], popup="¡Aquí estás!").add_to(mapa)
    return mapa

def render_map(mapa):
    map_key = f"mapa_{st.session_state['latitude']}_{st.session_state['longitude']}"
    st_folium(mapa, width=700, height=500, key=map_key)

def init_session_state():
    if "map_initialized" not in st.session_state:
        st.session_state["map_initialized"] = False
        st.session_state["latitude"] = MADRID_SOL.get("lat")
        st.session_state["longitude"] = MADRID_SOL.get("lon")

def get_location():
    location = current_position()
    if not location:
        logger.warning("Current location not found, displaying default location MADRID PUERTA DEL SOL")
        return MADRID_SOL.get('lat'), MADRID_SOL.get('lon'), 100
    else:
        st.write(
            f"""Tu ubicación es 
            Latitud: {location.get('latitude', 'N/A')}
            Longitud: {location.get('longitude', 'N/A')}
            """
        )
        latitude = location.get('latitude', 'N/A')
        longitude = location.get('longitude', 'N/A')
        accuracy = 100

        if None in (latitude, longitude, accuracy):
            raise LocationError(
                "Faltan datos de ubicación.",
                location_data=location
            )
        else:
            logger.info(f"Ubicación obtenida: Latitud: {latitude}, Longitud: {longitude}, Accuracy: {accuracy}")
            return latitude, longitude, accuracy

def show_nearby_parking_lots(latitude, longitude):
    mapa = create_map(latitude, longitude, zoom_start=15, add_marker=True)

    radio_distancia_metros = 1000

    sql_query = text(f"""
                with cte_calculo AS (
                        select
                            distrito, barrio,
                            calle, num_finca, color,
                            bateria_linea, num_plazas,
                            gis_x, gis_y,
                            ST_X(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x::double precision, gis_y::double precision), 25830), 4326)) AS longitud,
                            ST_Y(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x::double precision, gis_y::double precision), 25830), 4326)) AS latitud
                        from public.calles_zona_ser_formatted
                )
                select 
                    *,
                    ST_Distance(
                        ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography,
                        ST_SetSRID(ST_MakePoint(cte.longitud, cte.latitud), 4326)::geography
                    ) AS distancia_metros  
                from cte_calculo cte
                where ST_Distance(
                        ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geography,
                        ST_SetSRID(ST_MakePoint(cte.longitud, cte.latitud), 4326)::geography
                    ) <= {radio_distancia_metros} and color like '%Azul%'
                order by distancia_metros; 
            """)

    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            result = conn.execute(sql_query)

            logger.info(f"EXECUTED QUERY: {sql_query}\n\n")

            rows = result.fetchall()

            if rows:
                total_lat = 0
                total_lon = 0
                marker_count = 0

                image_path = "assets/google-maps.jpeg"
                if os.path.exists(image_path):
                    st.image(image_path, width=100)

                for row in rows:
                    distrito, barrio, calle, num_finca, color, bateria_linea, num_plazas, gis_x, gis_y, longitud, latitud, distancia_metros = row
                    logger.info(f"Parking lot: {row}")
                    directions_url = f"https://www.google.com/maps/dir/?api=1&origin={latitude},{longitude}&destination={latitud},{longitud}"

                    popup_content = f"""
                    <b>Parking:{calle.replace('.', '')}, Nº{num_finca} ({barrio})</b><br>
                    <i>Distancia: {round(int(distancia_metros))} metros</i><br>
                    <b>Plazas:</b> {round(num_plazas)}<br>
                    <b>Batería:</b> {bateria_linea}
                    <p></p>
                    <a href="{directions_url}" target="_blank" style="background-color:#4285F4; color:white; padding: 10px 20px; text-align: center; display: inline-block; text-decoration: none; border-radius: 5px;">
                        Ver ruta en Google Maps
                    </a>
                    """

                    marker_icon = folium.Icon(
                        icon='fa-car-side',
                        prefix='fa',
                        color='lightblue',
                        icon_color='white'
                    )

                    folium.Marker(
                        location=[latitud, longitud],
                        popup=folium.Popup(popup_content, max_width=300),
                        icon=marker_icon
                    ).add_to(mapa)

                    total_lat += latitud
                    total_lon += longitud
                    marker_count += 1

                if marker_count > 0:
                    avg_lat = total_lat / marker_count
                    avg_lon = total_lon / marker_count
                    mapa.location = [avg_lat, avg_lon]

                render_map(mapa)
            else:
                logger.info(f"No nearby blue parking lots found at {radio_distancia_metros} m from your current location lat:{latitude}, lon:{longitude}")
                st.write(f"No hay aparcamientos azules cercanos a {radio_distancia_metros} metros de tu posición.")
                render_map(mapa)
    except Exception as e:
        logger.error(e)

def main():
    init_session_state()
    try:
        # lat, long, accuracy = get_location()
        lat, long, accuracy = MADRID_SOL.get('lat'),  MADRID_SOL.get('lon'), 0

        st.write(f"Ubicación obtenida: Latitud: {lat}, Longitud: {long}, Accuracy: {accuracy}")

        show_nearby_parking_lots(lat, long)

    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()
