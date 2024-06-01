import logging
import socket
from dnslib import DNSRecord

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dns_client")


def query_dns_server(dns_domain, dns_qtype, dns_server, port):
    try:
        query = DNSRecord.question(dns_domain, dns_qtype)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(query.pack(), (dns_server, port))

        data, _ = sock.recvfrom(512)
        response = DNSRecord.parse(data)
        logger.info(f"Received response: {response}")
        print(response)
    except Exception as e:
        logger.error(f"Failed to query DNS server: {e}")



