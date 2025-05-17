import streamlit as st
from services.LocationService import LocationService
from services.ParkingService import ParkingService
from services.MapService import MapService
from services.DeviceService import DeviceService
from shared.utils.Logger import get_logger
from shared.utils.Map import init_session_state
from shared.utils.Layout import render_main_title

def main():
    # Inicializar servicios
    render_main_title()
    logger = get_logger()
    device_service = DeviceService()
    location_service = LocationService(logger)
    parking_service = ParkingService(logger)
    map_service = MapService(logger)

    # # Detectar dispositivo
    device_service.detect_device()

    # Detectar ubicación inicial
    user_location = location_service.detect_location()

    # Buscar otra ubicación si el usuario quiere
    search_input = st.text_input("🔍 Buscar otra ubicación (opcional):", placeholder="Ej. Nuevos Ministerios...")
    if search_input:
        user_location = location_service.search_location(search_input)
    init_session_state()
    latitude = user_location.latitude
    longitude = user_location.longitude

    # Mostrar resultados según dispositivo
    if st.session_state["is_mobile"]:
        nearby = parking_service.get_nearby_parking_lots(latitude, longitude)
        map_service.render_nearby_lots(nearby, latitude, longitude)

        nearest = parking_service.get_nearest_parking_lot(latitude, longitude)
        map_service.render_nearest_lot_summary(nearest, latitude, longitude)
    else:
        col1, col2 = st.columns([1, 2])
        with col1:
            nearest = parking_service.get_nearest_parking_lot(latitude, longitude)
            map_service.render_nearest_lot_summary(nearest, latitude, longitude)
        with col2:
            nearby = parking_service.get_nearby_parking_lots(latitude, longitude)
            map_service.render_nearby_lots(nearby, latitude, longitude)

if __name__ == "__main__":
    main()
