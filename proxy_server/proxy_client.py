import socket
from proxy_server.proxy import ProxyServer
import re


class ProxyClient():
    def __init__(self, host, port):
        self.port = port
        self.host = host if re.fullmatch(r"^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\."
                                         r"([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]):"
                                         r"((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})"
                                         r"|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$", host) else "127.0.0.1"

    def create_connection(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.bind((self.host, int(self.port)))
                client_socket.listen(10)
                proxy_server = ProxyServer()
                proxy_server.main_loop(client_socket)
        except Exception as e:
            print(e)
