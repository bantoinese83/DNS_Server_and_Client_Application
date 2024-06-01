import signal
import sys
import threading
import argparse
from time import sleep
from loguru import logger
from dns_server import start_dns_server, run_server
from dns_client import query_dns_server

# Configure logging
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")


# Start DNS server in a separate thread
def start_server():
    sock, port = start_dns_server()
    if sock:
        threading.Thread(target=run_server, args=(sock,), daemon=True).start()
        return port
    return None


def signal_handler(signum, frame):
    global stop_server
    stop_server = True
    logger.info("Stopping DNS Server")


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Server and Client Script")
    parser.add_argument("--mode", choices=["continuous", "on-demand"], default="continuous",
                        help="Mode to run the DNS server: 'continuous' or 'on-demand'")
    parser.add_argument("--queries", type=int, default=5,
                        help="Number of queries to perform in 'on-demand' mode")
    args = parser.parse_args()

    PORT = start_server()
    if not PORT:
        logger.error("Failed to start DNS server")
        sys.exit(1)

    logger.info(f"DNS Server started on port {PORT}")

    DOMAIN = "example.com"
    QTYPE = "A"
    SERVER = "127.0.0.1"

    stop_server = False

    if args.mode == "continuous":
        while not stop_server:
            try:
                query_dns_server(DOMAIN, QTYPE, SERVER, PORT)
                logger.info("DNS query completed")
            except Exception as e:
                logger.error(f"Failed to query DNS server: {e}")
            sleep(1)  # Wait for a second before the next query

    elif args.mode == "on-demand":
        for _ in range(args.queries):
            if stop_server:
                break
            try:
                query_dns_server(DOMAIN, QTYPE, SERVER, PORT)
                logger.info("DNS query completed")
            except Exception as e:
                logger.error(f"Failed to query DNS server: {e}")
            sleep(1)  # Wait for a second before the next query

    logger.info("DNS Server stopped")
    sys.exit(0)  # Ensure the script exits cleanly
