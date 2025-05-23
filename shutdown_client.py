import logging
import os
import pika
import socket
from dotenv import load_dotenv


load_dotenv()
hostname = socket.gethostname()

logger = logging.getLogger('shutdown_client')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('shutdown_client.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def on_message(ch, method, properties, body):
    if body.decode() == f'Shutdown approved for {hostname}':
        print(f" [x] Shutdown approved for {hostname}")
        logger.info({'hostname': hostname, 'user': properties.headers.get('user')})
        os.system('shutdown -h now')

def monitor_shutdown_approvals():
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
