import pika
import os


def rabbit_connect():
    rabbit_user = os.environ.get("RABBITMQ_USER")
    rabbit_password = os.environ.get("RABBITMQ_PASSWORD")
    rabbit_host = os.environ.get("RABBITMQ_HOST")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbit_host,
            credentials=pika.PlainCredentials(rabbit_user, rabbit_password)
        )
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange='sobel', exchange_type='direct', durable=True, auto_delete=False)

    channel.queue_declare(queue='pre-sobel', durable=True)

    channel.queue_bind(exchange='sobel', queue='pre-sobel', routing_key='pre')

    return channel
