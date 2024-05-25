import time
import pika
import os


def rabbit_connect():
    rabbit_user = os.environ.get("RABBITMQ_USER")
    rabbit_password = os.environ.get("RABBITMQ_PASSWORD")
    rabbit_host = os.environ.get("RABBITMQ_HOST")

    def connect():
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=rabbit_host,
                    credentials=pika.PlainCredentials(
                        rabbit_user, rabbit_password),
                    heartbeat=60
                )
            )
            channel = connection.channel()

            channel.exchange_declare(
                exchange='sobel', exchange_type='direct', durable=True, auto_delete=False)

            channel.queue_declare(queue='post-sobel', durable=True)

            channel.queue_bind(exchange='sobel', queue='post-sobel',
                               routing_key='post')

            return channel
        except pika.exceptions.AMQPConnectionError:
            return None

    while True:
        channel = connect()
        if channel:
            break
        print("Failed to connect to RabbitMQ. Retrying in 5 seconds...")
        time.sleep(5)

    return channel