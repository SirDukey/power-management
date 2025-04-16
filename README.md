![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![rabbitmq](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white)
![docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

## Power management for approving host shutdown.

This is a toy project, I have chosen RabbitMQ in place of a traditional API & DB is to learn more about message queues.

### The problem scenario
A problem that I have encountered with using ssh is that it is possible to accidentally shutdown the incorrect host when connected multiple hosts.  A solution would be a request and approve (perhpaps by a colleague) approach.

### A solution using message queues
Instead of running the shutdown command on a host, it would be possible to run the script to request a shutdown, the request can be approved or denied and if approved the host can then shutdown.

Using RabbitMQ as a centralized message broker allows all hosts to only make outbound connections towards the RabbitMQ server on port 5672

### Usage

1. clone this repository
2. Install [uv](https://github.com/astral-sh/uv), then setup the project with `uv sync`
3. Start a RabbitMQ container using the [script](run-rabbit-container.sh)
4. use `uv run ...` for each script you wish to run

- `shutdown_client.py` - can be run on each host via systemd, it listens for approved shutdowns and executes the shutdown command.
- `request_shutdown.py` - can be used in place of the shutdown command to send a shutdown request.
- `approval_monitor.py` - checks for shutdown requests allowing you to approve or deny

### Future improvements:

An idea I have is to create a small API using FastAPI which would take the place of the `approval_monitor.py` script.  It could send an email or webhook message with an embeded approval link/button, when clicked the api request would then send the rabbit message.
