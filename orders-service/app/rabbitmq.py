import os
import json
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def publish_order_created(order_data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue="order_created", durable=False)
    channel.basic_publish(exchange="", routing_key="order_created", body=json.dumps(order_data))
    connection.close()
