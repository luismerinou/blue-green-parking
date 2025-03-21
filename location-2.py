import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import requests
import folium
from streamlit_folium import st_folium

# Crear una aplicación Flask embebida
app = Flask(__name__)
CORS(app, origins=["http://localhost:8501", "http://127.0.0.1:8501"], methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])

# Variable para almacenar las coordenadas recibidas
received_coordinates = {"latitude": None, "longitude": None}

@app.route("/save_location", methods=["POST"])
def save_location():
    global received_coordinates
    data = request.json
    received_coordinates["latitude"] = data.get("latitude")
    received_coordinates["longitude"] = data.get("longitude")
    return jsonify({"message": "Ubicación guardada correctamente"})

@app.route("/get_location", methods=["GET"])
def get_location():
    return jsonify(received_coordinates)

# Iniciar Flask en un hilo separado para no bloquear Streamlit
if "flask_thread" not in st.session_state:
    def run_flask():
        app.run(port=8000, debug=False)

    thread = Thread(target=run_flask, daemon=True)
    thread.start()
    st.session_state["flask_thread"] = thread

# Interfaz HTML con JavaScript para capturar la ubicación
html_code = """
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

                    // Actualizar el elemento HTML
                    const locationElement = document.getElementById("location");
                    locationElement.innerHTML = `Latitud: ${latitude}, Longitud: ${longitude}`;

                    // Enviar coordenadas al backend Python
                    fetch("http://localhost:8000/save_location", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ latitude, longitude })
                    }).then(response => response.json())
                      .then(data => console.log("Respuesta del servidor:", data))
                      .catch(error => console.error("Error:", error));
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
"""

# Renderizar la interfaz HTML en Streamlit
st.title("Mapa de Geolocalización con Streamlit-Folium")
st.components.v1.html(html_code, height=300)

# Consultar periódicamente las coordenadas desde la API de Flask
st.write("Obteniendo coordenadas en tiempo real...")
try:
    response = requests.get("http://localhost:8000/get_location")
    if response.status_code == 200:
        coordinates = response.json()
        latitude = coordinates.get("latitude")
        longitude = coordinates.get("longitude")

        if latitude and longitude:
            st.write("Coordenadas recibidas:")
            st.write(f"Latitud: {latitude}")
            st.write(f"Longitud: {longitude}")

            # Crear un mapa con Folium
            mapa = folium.Map(
                location=[latitude, longitude],
                zoom_start=15,
                control_scale=True  # Agrega la escala de control en el mapa
            )
            folium.Marker(
                [latitude, longitude],
                popup="Ubicación actual"
            ).add_to(mapa)

            # Mostrar el mapa en Streamlit
            st_folium(mapa, width=700, height=500)
        else:
            st.write("Pulsa el botón para capturar tu ubicación.")
except requests.ConnectionError:
    st.error("No se pudo conectar al servidor Flask. Asegúrate de que Flask está ejecutándose.")
