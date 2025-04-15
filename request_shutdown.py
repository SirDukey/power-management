import os
import pika
import socket
from dotenv import load_dotenv


load_dotenv()

def send_shutdown_request(hostname):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_HOST', 'localhost')))
    channel = connection.channel()
    queue_name = f'{hostname}_shutdown_requests'
    channel.queue_declare(queue=queue_name),
    properties=pika.BasicProperties(
        expiration=str(int(os.getenv('MESSAGE_TTL', 60) * 1000))
        )

    channel.basic_publish(
        exchange='', 
        routing_key=queue_name, 
        body=f'Shutdown request for {hostname}',
        properties=properties
    )
    print(f" [x] Sent 'Shutdown request for {hostname}'")
    connection.close()

hostname = socket.gethostname()
send_shutdown_request(hostname)
