import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_available_port(start_port, end_port):
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('localhost', port))
                logger.info(f"Found available port: {port}")
                return port
            except OSError:
                logger.warning(f"Port {port} is in use")
                continue
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                break
    logger.error("No available port found in the range {}-{}".format(start_port, end_port))
    return None
