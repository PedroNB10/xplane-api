import time
from flask import Flask, jsonify
from waitress import serve
import xpc

APP_PORT = 8080

# Variável para armazenar o cliente do XPlaneConnect
client = None

# DREFs que serão consultados
drefs = [
    "sim/flightmodel/position/latitude",
    "sim/flightmodel/position/longitude",
    "sim/cockpit2/gauges/indicators/vvi_fpm_pilot",
    "sim/flightmodel/position/groundspeed",
    "sim/flightmodel/position/elevation",
    "sim/flightmodel2/position/mag_psi",
]


# Função para conectar ao X-Plane e tentar pegar os valores
def connect_to_xplane():
    global client
    while client is None:
        try:
            client = xpc.XPlaneConnect()
            print("Connected to X-Plane, verifying data...")

            # Testa se consegue obter os valores
            values = client.getDREFs(drefs)
            if all(v is not None for v in values):
                print("Successfully retrieved data from X-Plane!")
                return True
            else:
                raise ValueError("Data retrieval failed, retrying...")

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
                "speed": values[3][0],
                "altitude": values[4][0],
                "heading": values[5][0],
            }
        except:
            return {
                "latitude": 0,
                "longitude": 0,
                "vertical_speed": 0,
                "speed": 0,
                "altitude": 0,
                "heading": 0,
            }
    else:
        return {
            "latitude": 0,
            "longitude": 0,
            "vertical_speed": 0,
            "speed": 0,
            "altitude": 0,
            "heading": 0,
        }


app = Flask(__name__)


# Rota para a API
@app.route("/", methods=["GET"])
def get_api():
    data = get_xplane_data()
    return jsonify(data)


if __name__ == "__main__":
    # Conectar ao X-Plane antes de iniciar o servidor
    if connect_to_xplane():
        print(f"Server is running on http://localhost:{APP_PORT}")
        serve(app, host="0.0.0.0", port=APP_PORT)
    else:
        print("Could not connect to X-Plane or retrieve data.")
