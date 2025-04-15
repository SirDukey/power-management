import pika


def on_message(ch, method, properties, body):
    hostname = body.decode().split()[-1]
    print(f" [x] Received shutdown request for {hostname}")
    approval = input(f"Do you approve the shutdown for {hostname}? (yes/no): ").strip().lower()
    if approval == 'yes':
        send_approval(hostname)
    else:
        print(f" [x] Shutdown request for {hostname} denied")

def send_approval(hostname):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue_name = f'{hostname}_shutdown_approvals'
    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=f'Shutdown approved for {hostname}')
    print(f" [x] Sent 'Shutdown approved for {hostname}'")
    connection.close()

def monitor_shutdown_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # List of hostnames to monitor
    hostnames = ['ws-nlix-136.local']  # Add your hostnames here

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
