import socket
from cache import Cache
from packet_parser import *

localhost = '127.0.0.1'
port = 53


def launch_server():
    google_dns_ip = '8.8.8.8'
    cache = Cache()
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind((localhost, port))
            data, address = s.recvfrom(1024)
            parsed_request = PacketParser(data)
            record_from_cache = cache.get_record((parsed_request.qname, parsed_request.qtype))
            if record_from_cache is not None:
                print("Response from cache")
                response = parsed_request.get_response(record_from_cache)
                s.sendto(response, address)
            else:
                print("Response from DNS server")
                dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                dns.sendto(data, (google_dns_ip, port))
                google_data = dns.recvfrom(1024)[0]
                s.sendto(google_data, address)
                parsed_answer = PacketParser(google_data)
                for info in parsed_answer.info:
                    cache.add(*info)
        except KeyboardInterrupt:
            break
        finally:
            cache.caching()


if __name__ == "__main__":
    launch_server()
