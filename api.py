import time
from flask import Flask, jsonify
import xpc
import threading
import pytz
from datetime import datetime

APP_PORT = 8080

# Variável para armazenar o cliente do XPlaneConnect
client = None

# DREFs que serão consultados
drefs = [
    "sim/flightmodel/position/latitude",  # Latitude
    "sim/flightmodel/position/longitude",  # Longitude
    "sim/cockpit2/gauges/indicators/vvi_fpm_pilot",  # Vertical Speed
    "sim/flightmodel/position/groundspeed",  # Speed
    "sim/flightmodel/position/elevation",  # Altitude
    "sim/flightmodel2/position/mag_psi",  # Heading
]


# Função para conectar ao X-Plane e tentar pegar os valores
def connect_to_xplane():
    global client
    # Enquanto o cliente não estiver conectado, tentar conectar
    while client is None:
        try:
            # Abrindo conexão via UDP XplaneConnect
            client = xpc.XPlaneConnect()
            print("Connected to X-Plane, verifying data...")

        except Exception as e:
            print(f"Error: {e}")
            print(
                "X-Plane not running or data retrieval failed, retrying in 2 seconds..."
            )
            client = None
            time.sleep(2)


# Função para obter os dados do X-Plane
def get_xplane_data():
    if client:
        try:
            values = client.getDREFs(drefs)
            return {
                "latitude": values[0][0],
                "longitude": values[1][0],
                "vertical_speed": values[2][0],
                "speed": values[3][0] * 1.94384,  # Convert m/s to knots,
                "altitude": values[4][0] * 3.28084,  # Convert meters to feet
                "heading": values[5][0],
                "timestamp": datetime.now(pytz.UTC).replace(microsecond=0).isoformat(),
            }
        except:
            return {
                "error": "Failed to retrieve data from X-Plane, please try again later"
            }

    return {"error": "The client is not connected to X-Plane"}


app = Flask(__name__)


# Rota para a API
@app.route("/", methods=["GET"])
def get_api():
    data = get_xplane_data()
    return jsonify(data)


if __name__ == "__main__":
    thr = threading.Thread(target=connect_to_xplane, args=(), kwargs={})
    thr.start()
    print(f"Server is running on http://localhost:{APP_PORT}")
    app.run(host="0.0.0.0", port=APP_PORT)
