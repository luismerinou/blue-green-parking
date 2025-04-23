import folium
from folium.features import DivIcon


def get_car_side_icon(color):
    color_map = {
        "azul": "#72C2E3",   # Azul claro
        "verde": "#7bb074",  # Verde
        "rojo": "#d95c5c",   # Rojo
        "naranja": "#f4a261",  # Naranja
        "alta rotación": "#e0bbff"
    }
    hex_color = color_map.get(color.lower(), "#ffffff")

    html_icon = f"""
    <div style="border-radius: 50%; background-color: {hex_color}; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
        <i class="fa fa-car-side" style="color:white; font-size:14px;"></i>
    </div>
    """
    return DivIcon(html=html_icon)

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