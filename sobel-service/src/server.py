import json
import threading
import time
import pika

from flask import Flask, jsonify
from utils.sobel_filter import filter_image
from plugins.rabbit_client import rabbit_connect
from plugins.storage_client import upload_image, download_image

app = Flask(__name__)

rabbitmq_channel = None


def get_rabbitmq_channel():
    global rabbitmq_channel
    if rabbitmq_channel is None:
        rabbitmq_channel = rabbit_connect()
    return rabbitmq_channel


def consume_tasks():
    rabbitmq_channel = get_rabbitmq_channel()
    print(" [*] Waiting for messages. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        subtask = json.loads(body)
        fragment = subtask["fragment_name"]

        # Descargo fragmento original del bucket
        download_image(fragment)
        time.sleep(20)

        # Filtro el fragmento original descargado
        filter_image(fragment)
        time.sleep(15)

        # Subo el fragmento sobelizado al bucket
        upload_image(fragment)

        # Registrar subtask en rabbitmq para join-service
        new_subtask = {
            "task_id": subtask["task_id"],
            "subtask_id": subtask["subtask_id"],
            "fragment_name": fragment,
        }

        properties = pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)

        rabbitmq_channel.basic_publish(
            exchange='sobel', routing_key='post',
            properties=properties,
            body=json.dumps(new_subtask))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    rabbitmq_channel.basic_consume(
        queue='pre-sobel', on_message_callback=callback)
    rabbitmq_channel.start_consuming()


@app.route("/api/status", methods=['GET'])
def status():
    return jsonify({"code": "200", "status": "OK", "description": "Sobel service is working..."})


# Iniciar el consumidor al arrancar la aplicación Flask
time.sleep(15)
consumer_thread = threading.Thread(target=consume_tasks)
consumer_thread.start()
