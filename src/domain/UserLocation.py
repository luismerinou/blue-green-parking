class UserLocation:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def update_location(self, latitude: float, longitude: float):
        """Actualiza la ubicación del usuario"""
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<UserLocation lat={self.latitude} lon={self.longitude}>"
