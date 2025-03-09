import branca
import folium

m = folium.Map([43, -100], zoom_start=4)

html = """
    <h1> This is a big popup</h1><br>
    With a few lines of code...
    <p>
    <code>
        from numpy import *<br>
        exp(-2*pi)
    </code>
    </p>
    """


folium.Marker([30, -100], popup=html).add_to(m)

m