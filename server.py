from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://localhost", "http://127.0.0.1"], methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])

coordinates = {"latitude": None, "longitude": None}

@app.route("/save_location", methods=["POST"])
def save_location():
    """
    Guarda las coordenadas recibidas del cliente.
    """
    data = request.json
    coordinates["latitude"] = data.get("latitude")
    coordinates["longitude"] = data.get("longitude")
    return jsonify({"message": "Ubicación guardada correctamente"})

@app.route("/get_location", methods=["GET"])
def get_location():
    """
    Devuelve las coordenadas actuales.
    """
    return jsonify(coordinates)

if __name__ == "__main__":
    if "flask_thread" not in st.session_state:
        def run_flask():
            app.run(port=8000, debug=False)

        thread = Thread(target=run_flask, daemon=True)
        thread.start()
        st.session_state["flask_thread"] = thread
