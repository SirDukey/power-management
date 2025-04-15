## Power management for approving host shutdown.

A problem that I have encountered with using ssh is that it is possible to accidentally shutdown the incorrect host when connected multiple hosts.  A solution would be a request and approve (perhpaps by a colleague) approach.

Instead of running the shutdown command on a host, it would be possible to run the script to request a shutdown, the request can be approved or denied and if approved the host can then shutdown.

Using RabbitMQ as a centralized message broker allows all hosts to only make outbound connections towards the RabbitMQ server on port 5672

### Usage

Start a RabbitMQ container first then use the following scripts with `uv run ...`

- `shutdown_client.py` - can be run on each host via systemd, it listens for approved shutdowns and executes the shutdown command.
- `request_shutdown.py` - can be used in place of the shutdown command to send a shutdown request.
- `approval_monitor.py` - checks for shutdown requests allowing you to approve or deny

### Future improvements:
Integrate a way of signing the approval and writing the event to either a log or sqlite.  If using a log file then it could then be forwarded to a logging server like Loki or Fluentd

An idea I have is to create a small API using FastAPI which would take the place of the `approval_monitor.py` script.  It could send an email or webhook message with an embeded approval link/button, when clicked the api request would then send the rabbit message