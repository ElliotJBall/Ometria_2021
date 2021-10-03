import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

from . import importer

# FIXME: REMEMBER TO SET THESE TO INFO BEFORE MAKING AVAILABLE
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logging.getLogger("").addHandler(ch)


class MockServer(BaseHTTPRequestHandler):
    def do_POST(self):
        # If we actually used a REST API here this would be async and return 202
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"status": 200, "message": "Starting the import!"}).encode()
        )

        importer.run_import()


if __name__ == "__main__":
    logger.info(
        "Let's pretend this is the HTTP endpoint is instead some message broker/task queue (RabbitMQ, Kafka)...Send a "
        "POST request to simulate receiving a message from the message broker!"
    )

    server = HTTPServer(("localhost", 8080), MockServer)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
