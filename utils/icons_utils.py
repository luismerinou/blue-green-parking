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
