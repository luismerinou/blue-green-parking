from threading import Thread
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from utils.get_html_code import get_html_code
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://localhost", "http://127.0.0.1"], methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])

current_location = {"latitude": None, "longitude": None}

@app.route("/save_location", methods=["POST"])
def save_location():
    global current_location
    data = request.json
    current_location["latitude"] = data.get("latitude")
    current_location["longitude"] = data.get("longitude")
    return jsonify({"message": "Ubicación guardada correctamente"})

@app.route("/get_location", methods=["GET"])
def get_location():
    return jsonify(current_location)

if "flask_thread" not in st.session_state:
    def run_flask():
        app.run(port=8000, debug=False)

    thread = Thread(target=run_flask, daemon=True)
    thread.start()
    st.session_state["flask_thread"] = thread


st.title("Mapa de Geolocalización con Streamlit y Flask")

html_code = get_html_code()
st.components.v1.html(html_code, height=300)

try:
    response = requests.get("http://localhost:8000/get_location")
    if response.status_code == 200:
        coordinates = response.json()
        latitude = coordinates.get("latitude")
        longitude = coordinates.get("longitude")

        if latitude and longitude:
            st.write("Coordenadas recibidas:")
            st.write(f"Latitud: {latitude}, Longitud: {longitude}")

            # Crear y mostrar un mapa con Folium
            mapa = folium.Map(location=[latitude, longitude], zoom_start=15)
            folium.Marker([latitude, longitude], popup="Ubicación actual").add_to(mapa)
            st_folium(mapa, width=700, height=500)
        else:
            st.write("Pulsa el botón para capturar tu ubicación.")
except requests.ConnectionError:
    st.error("No se pudo conectar al servidor Flask. Asegúrate de que Flask está ejecutándose.")
