import streamlit as st
from bs4 import BeautifulSoup


# HTML y JavaScript para obtener la ubicación
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Geolocalización Precisa</title>
</head>
<body>
    <h2>Obtén tu ubicación precisa</h2>
    <button onclick="getLocation()">Mostrar mi ubicación</button>
    <p id="location"></p>
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
            } else {
                document.getElementById("location").innerHTML = "Geolocalización no es soportada en este navegador.";
            }
        }

        function showPosition(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            document.getElementById("location").innerHTML = `Latitud: ${lat}, Longitud: ${lon}`;
            
            // Enviar coordenadas a la aplicación Streamlit
            const streamlitAPI = window.parent.streamlit;
            streamlitAPI.setComponentValue({latitude: lat, longitude: lon});
        }

        function showError(error) {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    document.getElementById("location").innerHTML = "Permiso denegado.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    document.getElementById("location").innerHTML = "Ubicación no disponible.";
                    break;
                case error.TIMEOUT:
                    document.getElementById("location").innerHTML = "Tiempo de espera agotado.";
                    break;
                default:
                    document.getElementById("location").innerHTML = "Ocurrió un error desconocido.";
            }
        }
    </script>
</body>
</html>
"""

# Crear la aplicación de Streamlit
st.title("Aplicación de Geolocalización Precisa")

st.markdown("Esta aplicación usa la API de geolocalización del navegador para obtener tu ubicación precisa.")
st.components.v1.html(html_code, height=400)



# HTML en el que queremos buscar
html_content = """
<p id="location">
"""

# Crear el objeto BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Buscar el elemento por su atributo id
location_element = soup.find('p', id='location')

# Verificar si se encontró el elemento y obtener su contenido
if location_element:
    location_text = location_element.get_text()
    print(f"Contenido del elemento: {location_text}")
    
    # Procesar el texto para extraer latitud y longitud
    lat_lon = location_text.replace("Latitud:", "").replace("Longitud:", "").split(',')
    latitude = float(lat_lon[0].strip())
    longitude = float(lat_lon[1].strip())
    print(f"Latitud: {latitude}, Longitud: {longitude}")
    st.write(f"Latitud: {latitude}, Longitud: {longitude}")
else:
    print("Elemento no encontrado.")
    st.write("Elemento no encontrado.")
