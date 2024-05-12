import os
import requests
import imghdr
import uuid

from flask import Flask, jsonify, request, send_file
from storage_client import check_result


app = Flask(__name__)


@app.route("/api/status", methods=['GET'])
def status():
    return jsonify({"code": "200", "status": "OK", "description": "Entry server is working..."})


@app.route("/api/result/<task_id>", methods=['GET'])
# A este endpoint le pega el cliente para saber si su resultado ya está disponible
def getResult(task_id):
    if request.method == 'GET':
        # TODO: Buscar en el bucket si está la imagen resultado.
        url = check_result(task_id)
        if (url):
            return jsonify({'COMPLETED': f"El resultado sobel de la imagen {task_id} ya está disponible", 'URL': url}), 200
        else:
            return jsonify({'PENDING': f"El resultado sobel de la imagen {task_id} aún no está disponible. Vuelva en unos momentos"}), 200
    else:
        return jsonify({'Method not allowed': 'Método no permitido'}), 405


@app.route("/api/result/<task_id>", methods=['POST'])
# A este endpoint le pega el join-service cuando tiene la imagen sobel final
def storeResult(task_id):
    if request.method == 'POST':
        image_file = request.files['image']
        image_data = image_file.read()
        file_name = f"{task_id}.png"

        os.makedirs("results", exist_ok=True)

        with open(os.path.join("results", file_name), 'wb') as f:
            f.write(image_data)
        return jsonify({'OK': f"Resultado sobel de la imagen {task_id} almacenado correctamente"}), 200
    else:
        return jsonify({'Method not allowed': 'Método no permitido'}), 405


@app.route("/api/sobel", methods=['POST'])
# A este endpoint le pega el cliente con la imagen original para iniciar el proceso sobel
def sobel():
    if request.method == 'POST':
        # Verifica si hay un archivo adjunto de imagen en la solicitud
        try:
            if 'image' in request.files:
                # Obtén el archivo adjunto de la imagen
                image_file = request.files['image']

                # Lee los datos binarios de la imagen
                image_data = image_file.read()

                # Verifica si el archivo adjunto es realmente una imagen
                image_type = imghdr.what(None, h=image_data)

                if image_type not in ['jpeg', 'png', 'bmp', 'jpg']:
                    return jsonify({'Bad request': 'Formato de imagen no válido. Solo se permiten archivos PNG, JPG o BMP.'}), 400

                task_id = str(uuid.uuid4())

                # Envía la imagen al splitter
                url = os.environ.get('SPLIT_SERVICE_URL')
                url = f"{url}/{task_id}"

                response = requests.post(
                    url, files={"image": image_data})

                if response.status_code == 200:
                    return jsonify({'OK': "Proceso sobel iniciado", 'TASK_ID': task_id}), 200
                else:
                    return jsonify({'Internal server error': 'Ocurrió un error al procesar la imagen. Reintente en unos momentos.'}), 500
        except internal_server_error as e:
            print(e)
            return jsonify({'Internal server error': 'Ocurrió un error al procesar la imagen. Reintente en unos momentos.'}), 500
    else:
        return jsonify({'Method not allowed': 'Método no permitido'}), 405


@app.errorhandler(500)
def internal_server_error(error):
    print("Se ha producido un error interno del servidor:", error)
