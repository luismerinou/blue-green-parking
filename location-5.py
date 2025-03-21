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

MADRID_SOL = {
    "lon": -3.702247,  # Longitud de Madrid
    "lat": 40.419839   # Latitud de Madrid
}

# Variable global para almacenar las coordenadas recibidas
global received_coordinates
received_coordinates = {"latitude": None, "longitude": None}

@app.route("/save_location", methods=["POST"])
def save_location():
    """
    Endpoint para guardar coordenadas enviadas desde el navegador.
    """
    data = request.json
    received_coordinates["latitude"] = data.get("latitude")
    received_coordinates["longitude"] = data.get("longitude")
    return jsonify({"message": "Ubicación guardada correctamente"})

@app.route("/get_location", methods=["GET"])
def get_location():
    """
    Endpoint para devolver las coordenadas almacenadas.
    """
    return jsonify(received_coordinates)

# Iniciar Flask en un hilo separado para no bloquear Streamlit
if "flask_thread" not in st.session_state:
    def run_flask():
        app.run(port=8000, debug=False)
    
    thread = Thread(target=run_flask, daemon=True)
    thread.start()
    st.session_state["flask_thread"] = thread

# Función para obtener coordenadas del endpoint Flask
def get_coordinates():
    try:
        response = requests.get("http://localhost:8000/get_location")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener coordenadas: {response.status_code}")
            return {"latitude": None, "longitude": None}
    except requests.ConnectionError:
        st.error("Error al conectar con el servidor Flask.")
        return {"latitude": None, "longitude": None}

# Título de la aplicación
st.title("Mapa con Solicitud de Ubicación")

# Manejo de inicialización del mapa
if "map_initialized" not in st.session_state:
    st.session_state["map_initialized"] = False
    st.session_state["latitude"] = MADRID_SOL["lat"]
    st.session_state["longitude"] = MADRID_SOL["lon"]

# Botón de Streamlit para actualizar la ubicación
if st.button("Actualizar mi ubicación"):
    coordinates = get_coordinates()
    if coordinates["latitude"] and coordinates["longitude"]:
        st.session_state["latitude"] = coordinates["latitude"]
        st.session_state["longitude"] = coordinates["longitude"]
        st.session_state["map_initialized"] = True
        st.success("Ubicación actualizada.")

# Botón de Streamlit para centrar el mapa
if st.button("Centrar en mi ubicación"):
    if st.session_state["latitude"] and st.session_state["longitude"]:
        st.session_state["map_initialized"] = True
    else:
        st.warning("No se han obtenido coordenadas válidas aún.")

# Renderizar mapa en Streamlit
st.write("Mapa:")
if st.session_state["map_initialized"]:
    latitude = st.session_state["latitude"]
    longitude = st.session_state["longitude"]
    # Crear un mapa centrado en las coordenadas actuales
    mapa = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude, longitude], popup="¡Aquí estás!").add_to(mapa)
    # Mostrar el mapa
    st_folium(mapa, width=700, height=500, key="mapa_actualizado")
else:
    # Mostrar mapa vacío (si no se han inicializado coordenadas)
    mapa_vacio = folium.Map(location=[MADRID_SOL["lat"], MADRID_SOL["lon"]], zoom_start=13)
    st_folium(mapa_vacio, width=700, height=500, key="mapa_vacio")

# Usar geolocalización nativa con Streamlit (usando JavaScript con el componente de HTML)
if st.button("Solicitar mi ubicación"):
    st.warning("Esperando por tu ubicación...")
    html_code = """
    <script>
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                // Enviar las coordenadas al backend Flask
                fetch("http://localhost:8000/save_location", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ latitude, longitude })
                }).then(response => response.json())
                .then(data => {
                    // Recargar la página para actualizar el mapa con las nuevas coordenadas
                    window.location.reload();
                })
                .catch(error => console.error("Error al enviar las coordenadas:", error));
            }, (error) => {
                alert("Error al obtener la ubicación: " + error.message);
            });
        } else {
            alert("Geolocalización no soportada por este navegador.");
        }
    </script>
    """
    st.components.v1.html(html_code)
