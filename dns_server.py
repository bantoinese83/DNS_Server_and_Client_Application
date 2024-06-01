import logging
import socket
from dnslib import DNSRecord, QTYPE, RR, A, AAAA, CNAME
from util import find_available_port

# DNS Record configurations
DNS_ZONE = {
    "example.com.": {
        "A": "192.0.2.1",
        "AAAA": "2001:db8::1",
        "CNAME": "alias.example.com."
    },
    "test.com.": {
        "A": "192.0.2.2"
    }
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dns_server")


def handle_dns_query(data, addr, sock):
    try:
        request = DNSRecord.parse(data)
        response = DNSRecord(request.header)
        response.add_question(request.q)

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        logger.info(f"Received query for {qname} of type {qtype}")

        if qname in DNS_ZONE and qtype in DNS_ZONE[qname]:
            if qtype == 'A':
                response.add_answer(RR(qname, QTYPE.A, rdata=A(DNS_ZONE[qname][qtype]), ttl=60))
            elif qtype == 'AAAA':
                response.add_answer(RR(qname, QTYPE.AAAA, rdata=AAAA(DNS_ZONE[qname][qtype]), ttl=60))
            elif qtype == 'CNAME':
                response.add_answer(RR(qname, QTYPE.CNAME, rdata=CNAME(DNS_ZONE[qname][qtype]), ttl=60))
            logger.info(f"Answered: {qname} -> {DNS_ZONE[qname][qtype]}")
        else:
            logger.warning(f"No record for {qname} of type {qtype}")

        sock.sendto(response.pack(), addr)
    except Exception as e:
        logger.error(f"Failed to handle query: {e}")


def start_dns_server(host='0.0.0.0', start_port=1024, end_port=65535):
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = find_available_port(start_port, end_port)
    if port is None:
        logger.error("No available port found in the range {}-{}".format(start_port, end_port))
        return None, None

    _sock.bind((host, port))
    logger.info(f"DNS Server started on {host}:{port}")
    return _sock, port


def run_server(sock):
    while True:
        data, addr = sock.recvfrom(512)
        handle_dns_query(data, addr, sock)
