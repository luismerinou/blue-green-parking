import folium


def get_car_side_icon():
    return folium.Icon(
        icon="fa-car-side", prefix="fa", color="lightblue", icon_color="white"
    )

def get_my_location_icon():
    return folium.Icon(
        icon="fa-solid fa-location-crosshairs", prefix="fa", color="red", icon_color="white"
    )

def get_page_icon():
    return folium.Icon(
        icon="fa-solid fa-car-on", prefix="fa", color="blue", icon_color="white"
    )

def get_pop_up_content(calle, num_finca, barrio, distancia_metros, num_plazas, bateria_linea, directions_url):
    return f"""
            <b>Parking:{calle.replace(".", "")}, Nº{num_finca} ({barrio})</b><br>
            <i>Distancia: {round(int(distancia_metros))} metros</i><br>
            <b>Plazas:</b> {round(num_plazas)}<br>
            <b>Batería:</b> {bateria_linea}
            <p></p>
            <a href="{directions_url}&travelmode=driving" target="_blank" style="background-color:#4285F4; color:white; padding: 10px 20px; text-align: center; display: inline-block; text-decoration: none; border-radius: 5px;">
                Ver ruta en Google Maps
            </a>
            """