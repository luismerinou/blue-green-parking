import streamlit as st
from domain.UserLocation import UserLocation
from shared.utils.Map import get_location_suggestions, geocode_location, get_location

class LocationService:
    def __init__(self, logger):
        self.logger = logger
        self.user_location = None

    def detect_location(self):
        """Detectar ubicación actual"""
        latitude, longitude = get_location(self.logger)
        self.user_location = UserLocation(latitude, longitude)
        return self.user_location

    def search_location(self, search_input):
        """Buscar una ubicación manualmente"""
        if search_input and len(search_input) >= 3:
            suggestions = get_location_suggestions(search_input)
            if suggestions:
                selected_place = st.selectbox("📍 Selecciona un destino", suggestions)
                if selected_place:
                    dest_lat, dest_lon = geocode_location(selected_place)
                    if dest_lat and dest_lon:
                        self.user_location.update_location(dest_lat, dest_lon)
                        return self.user_location
        return self.user_location
