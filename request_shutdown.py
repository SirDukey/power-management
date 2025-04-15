import pika
import socket


def send_shutdown_request(hostname):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue_name = f'{hostname}_shutdown_requests'
    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=f'Shutdown request for {hostname}')
    print(f" [x] Sent 'Shutdown request for {hostname}'")
    connection.close()

hostname = socket.gethostname()
send_shutdown_request(hostname)
