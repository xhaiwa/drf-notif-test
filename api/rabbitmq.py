import json
import pika
import os

from threading import Thread
from .models import Notification

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'user')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'pass')

def publish_event(event_type, data):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='book_created', exchange_type='fanout')

    message = json.dumps({
        'type': event_type,
        'data': data
    })
    channel.basic_publish(exchange='book_created', routing_key='', body=message)
    connection.close()

def start_consumer():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER, RABBITMQ_PASS
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials, heartbeat=600)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='book_created', exchange_type='fanout')
    channel.queue_declare(queue='book_created', durable=True)
    channel.queue_bind(exchange='book_created', queue='book_created')


    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Message reçu: {data}")

        notif = Notification(
            title=f"Nouveau livre: {data['data'].get('title')}",
            description=f"ID du livre: {data['data'].get('id')}"
        )
        notif.save()
        print(f"Notification créée avec id={notif.id}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='book_created', on_message_callback=callback)
    print("Consommateur RabbitMQ démarré")
    channel.start_consuming()
