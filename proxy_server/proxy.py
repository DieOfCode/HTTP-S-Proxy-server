import socket
from threading import Thread

import requests
import re
import proxy_server.errors

BUFFER_SIZE = 1024
PATH = "/home/frost"


class ProxyServer:
    def __init__(self):
        print('\n*********Server Start*********\n')
        self.port_regex = re.compile(
            r"(?P<type>\w{3,7}) (?P<address>(?P<https>(http://)?[_?a-zA-ZB0-9.-]+/*)*):?(?P<port>\d+)? .+")
        self.all_threads = set()

    def main_loop(self, socket):
        while True:
            client_socket, client_address = socket.accept()
            thread = Thread(target=self.handle_client_connection, args=(client_socket,), daemon=True)
            self.all_threads.add(thread)
            thread.start()

    def handle_client_connection(self, client_socket):
        client_data = b""
        while True:
            raw_data = client_socket.recv(BUFFER_SIZE)

            try:
                client_data += raw_data
            except UnicodeDecodeError:
                break
            if len(raw_data) < BUFFER_SIZE:
                break
        print(client_data)
        port, request_kind, web_server = self.parse_data(client_data)

        if request_kind == "GET":
            self.get_http_response(web_server, client_socket)
        else:
            self.get_https_response(web_server, port, client_socket)

    def parse_data(self, client_data):
        try:
            port = 443 if re.search(self.port_regex, str(client_data)).group("port") else 80
            web_server = re.search(self.port_regex, str(client_data)).group("address")
            request_kind = re.search(self.port_regex, str(client_data)).group("type")
            return port, request_kind, web_server
        except proxy_server.errors.ParserException as error:
            print(error.message)

    @staticmethod
    def get_http_response(web_server, client):
        try:
            print(web_server)
            client_request = requests.get(web_server)
            if client_request.status_code == 200:
                response = b"HTTP/1.1 200 OK\r\nProxy-Agent: myProxyServer\r\n\r\n"
                client.send(response)
                client.sendall(bytes(client_request.text.encode("utf-8")))
            else:
                response = b"HTTP/1.1 404 Not Found\r\nProxy-Agent: myProxyServer\r\n\r\nYour Website not Found\r\n"
                client.send(response)
        except requests.exceptions as error:
            print(error)
            return

    def get_https_response(self, web_server, port, client_socket):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as web_server_socket:
            try:
                host_ip = socket.gethostbyname(web_server)
                web_server_socket.connect((host_ip, port))
                client_socket.send(
                    "HTTP/1.1 200 Connection Established\r\nProxy-Agent: myProxyServer\r\n\r\n".encode("utf-8"))
                server_thread = Thread(target=self.send_data_to_server, args=(client_socket, web_server_socket),
                                       daemon=True)
                server_thread.setDaemon(True)
                server_thread.start()

                self.send_data_to_client(client_socket, web_server_socket)
            except socket.error as error:
                print(error)
                return

    @staticmethod
    def send_data_to_server(client_socket, server_socket: socket):
        try:
            while True:
                client_data = client_socket.recv(BUFFER_SIZE)
                server_socket.sendall(client_data)
                if len(client_data) < 1:
                    break
        except Exception as e:
            print(e)

    @staticmethod
    def send_data_to_client(client_socket, server_socket):
        try:
            while True:
                server_data = server_socket.recv(BUFFER_SIZE)
                client_socket.send(server_data)
                if len(server_data) < 1:
                    break
        except Exception as e:
            print(e)
