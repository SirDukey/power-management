import os
import pika
import socket
from dotenv import load_dotenv


load_dotenv()

def on_message(ch, method, properties, body):
    hostname = socket.gethostname()
    if body.decode() == f'Shutdown approved for {hostname}':
        print(f" [x] Shutdown approved for {hostname}")
        #os.system('shutdown -h now')

def monitor_shutdown_approvals():
    hostname = socket.gethostname()
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_HOST', 'localhost')))
    channel = connection.channel()
    queue_name = f'{hostname}_shutdown_approvals'
    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    print(f' [*] Waiting for approval messages for {hostname}. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        monitor_shutdown_approvals()
    except KeyboardInterrupt:
        print('\nExiting ...')
