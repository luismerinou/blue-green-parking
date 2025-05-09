from shared.utils.sql_utils import get_nearest_parking_lot_from_user, get_parking_lots_around_me
from domain.ParkingLots import ParkingLot

class ParkingService:
    def __init__(self, logger):
        """Inicializa el servicio con un logger para registrar eventos."""
        self.logger = logger

    def get_nearby_parking_lots(self, latitude, longitude, distance=500):
        """Obtiene una lista de aparcamientos cercanos a una ubicación dada."""
        raw_data = get_parking_lots_around_me(
            self.logger, distance_from_me=distance,
            current_longitude=longitude, current_latitude=latitude
        )
        return [self._map_to_parking_lot(data) for data in raw_data]

    def get_nearest_parking_lot(self, latitude, longitude, distance=1000):
        """Obtiene el aparcamiento más cercano a una ubicación dada."""
        raw_data = get_nearest_parking_lot_from_user(
            self.logger, distance_from_me=distance,
            current_longitude=longitude, current_latitude=latitude
        )
        if raw_data:
            return self._map_to_parking_lot(raw_data[0])
        return None

    def _map_to_parking_lot(self, data_row):
        """Transforma una fila de SQL en un ParkingLot"""
        (
            longitud,
            latitud,
            barrio,
            calle,
            num_finca,
            color,
            bateria_linea,
            num_plazas,
            distancia_metros,
        ) = data_row
        return ParkingLot(
            latitude=latitud,
            longitude=longitud,
            barrio=barrio,
            calle=calle,
            numero_finca=num_finca,
            color=color,
            bateria_linea=bateria_linea,
            num_plazas=num_plazas,
            distancia_metros=distancia_metros,
        )
