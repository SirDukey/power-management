import logging
import os
import pika
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger('approval_monitor')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('approval_monitor.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def get_rabbitmq_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_HOST', 'localhost')))

def on_message(ch, method, properties, body):
    hostname = body.decode().split()[-1]
    print(f" [x] Received shutdown request for {hostname}")
    approval = input(f"Do you approve the shutdown for {hostname}? (yes/no): ").strip().lower()
    if approval == 'yes':
        send_approval(hostname)
    else:
        print(f" [x] Shutdown request for {hostname} denied")
    logger.info({'hostname': hostname, 'approval': approval, 'user': os.getenv('USER')})

def send_approval(hostname):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    queue_name = f'{hostname}_shutdown_approvals'
    channel.queue_declare(queue=queue_name)
    properties=pika.BasicProperties(
        expiration=str(int(os.getenv('MESSAGE_TTL', 60) * 1000)),
        headers={'hostname': hostname, 'user': os.getenv('USER')}
    )

    channel.basic_publish(
        exchange='', 
        routing_key=queue_name, 
        body=f'Shutdown approved for {hostname}',
        properties=properties
    )
    print(f" [x] Sent 'Shutdown approved for {hostname}'")
    connection.close()

def monitor_shutdown_requests():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    hostnames = os.getenv('HOSTNAMES', 'localhost').split(',')

    for hostname in hostnames:
        queue_name = f'{hostname}_shutdown_requests'
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)

    print(' [*] Waiting for shutdown requests. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        monitor_shutdown_requests()
    except KeyboardInterrupt:
        print('\nExiting ...')
