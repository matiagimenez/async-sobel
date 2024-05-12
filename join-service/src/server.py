import io
import os
import json
import threading
import time


from flask import Flask, jsonify
from plugins.rabbitmq.rabbit_client import rabbit_connect
from plugins.redis.redis_client import redis_connect
from plugins.bucket.storage_client import download_image, upload_image
from utils.join import join_image

app = Flask(__name__)


redis_connection = None
rabbitmq_channel = None


def get_redis_connection():
    global redis_connection
    if redis_connection is None:
        redis_connection = redis_connect()
    return redis_connection


def get_rabbitmq_channel():
    global rabbitmq_channel
    if rabbitmq_channel is None:
        rabbitmq_channel = rabbit_connect()
    return rabbitmq_channel


@app.route("/api/status", methods=['GET'])
def status():
    return jsonify({"code": "200", "status": "OK", "description": "Join service is working..."})


def consume_tasks():
    r = get_redis_connection()
    rabbitmq_channel = get_rabbitmq_channel()
    print(" [*] Waiting for messages. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        subtask = json.loads(body)

        task_id = subtask["task_id"]

        task = r.hgetall(task_id)

        # Actualiza estado de tarea. Cada completed subtask = 1 fragmento sobelizado
        task["completed_subtasks"] = int(task["completed_subtasks"]) + 1

        if (int(task["completed_subtasks"]) == int(task["subtasks_count"])):
            task["status"] = "COMPLETED"
            task["completed_at"] = int(time.time())

            fragments = json.loads(task["fragments"])

            for fragment in fragments:
                # Descarga del bucket cada fragmento sobelizado asociado a la tarea
                download_image(fragment)

            time.sleep(30)

            join_image(fragments, task_id)

            time.sleep(20)

            # Sube la imagen final al bucket
            upload_image(task_id)

        r.hset(task_id, mapping=task)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    rabbitmq_channel.basic_consume(
        queue='post-sobel', on_message_callback=callback)
    rabbitmq_channel.start_consuming()


@ app.errorhandler(500)
def internal_server_error(error):
    print("Se ha producido un error interno del servidor:", error)
    return "Ocurrió un error interno del servidor", 500


# Iniciar el consumidor al arrancar la aplicación Flask
time.sleep(15)
consumer_thread = threading.Thread(target=consume_tasks)
consumer_thread.start()
