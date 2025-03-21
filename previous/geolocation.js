<!DOCTYPE html>
<html>
<head>
    <title>Geolocalización</title>
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    // Guardar en el elemento <p> y enviar datos a Streamlit
                    const locationElement = document.getElementById("location");
                    locationElement.innerHTML = `Latitud: ${latitude}, Longitud: ${longitude}`;

                    // Enviar coordenadas a Streamlit
                    window.parent.streamlit.setComponentValue({
                        latitude: latitude,
                        longitude: longitude
                    });
                }, (error) => {
                    console.error("Error al obtener la ubicación:", error);
                });
            } else {
                console.error("Geolocalización no soportada por este navegador.");
            }
        }
    </script>
</head>
<body>
    <h2>Geolocalización</h2>
    <button onclick="getLocation()">Mostrar mi ubicación</button>
    <p id="location">Pulsa el botón para mostrar tu ubicación</p>
</body>
</html>
