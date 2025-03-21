def get_html_code():
    """
    Devuelve el código HTML que incluye el botón y conecta el archivo JavaScript externo.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Geolocalización</title>
        <script src="http://localhost:8000/static/geolocation.js"></script>
    </head>
    <body>
        <h2>Geolocalización</h2>
        <button onclick="getLocation()">Mostrar mi ubicación</button>
        <p id="location">Pulsa el botón para mostrar tu ubicación</p>
    </body>
    </html>
    """
