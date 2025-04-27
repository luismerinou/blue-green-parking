from shared.utils.Map import create_map, render_map
from shared.utils.Icon import get_car_side_icon, get_pop_up_content
import folium
import streamlit as st

class MapService:
    def __init__(self, logger):
        """Inicializa el servicio de mapas con un logger para registrar eventos."""
        self.logger = logger

    def render_nearby_lots(self, parking_lots, user_lat, user_lon):
        """Renderiza en un mapa todos los aparcamientos cercanos al usuario."""
        mapa = create_map(user_lat, user_lon, zoom_start=15, add_marker=True)

        for parking in parking_lots:
            directions_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={parking.latitude},{parking.longitude}"
            popup = get_pop_up_content(parking.calle, parking.numero_finca, parking.barrio, parking.distancia_metros, parking.num_plazas, parking.bateria_linea, directions_url)
            folium.Marker(
                [parking.latitude, parking.longitude],
                popup=popup,
                icon=get_car_side_icon(parking.color),
            ).add_to(mapa)

        render_map(mapa)

    def render_nearest_lot_summary(self, parking, user_lat, user_lon):
        """Muestra un resumen visual del aparcamiento más cercano al usuario."""
        if not parking:
            st.warning("No se encontró ningún aparcamiento cercano.")
            return

        directions_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={parking.latitude},{parking.longitude}"
        st.markdown(f"""
        <div style="background-color:#1E1E1E; padding: 1rem; border-radius: 12px; margin-top: 1rem;">
            <h3 style="margin-bottom: 0.5rem;">🅿️ Aparcamiento más cercano</h3>
            <p>Tu aparcamiento más cercano está a <strong>{round(parking.distancia_metros, 0)}m</strong>, con <strong>{parking.num_plazas}</strong> plazas en zona <strong style="color:{'blue' if parking.color.lower() == 'azul' else 'green'};">{parking.color}</strong>.</p>
            <a href="{directions_url}" target="_blank" style="display:inline-block; background-color:#2563EB; color:white; padding:0.5rem 1rem; border-radius:8px; text-decoration:none; font-weight:600;">Ver en Google Maps</a>
        </div>
        """, unsafe_allow_html=True)
