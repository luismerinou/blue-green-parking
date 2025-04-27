class ParkingLot:
    def __init__(self, latitude: float, longitude: float, barrio: str, calle: str,
                 numero_finca: str, color: str, bateria_linea: str, num_plazas: int, distancia_metros: float):
        self.latitude = latitude
        self.longitude = longitude
        self.barrio = barrio
        self.calle = calle
        self.numero_finca = numero_finca
        self.color = color
        self.bateria_linea = bateria_linea
        self.num_plazas = num_plazas
        self.distancia_metros = distancia_metros

    def __repr__(self):
        return (f"<ParkingLot {self.calle} {self.numero_finca} "
                f"({self.barrio}) color={self.color} plazas={self.num_plazas}>")
