import socket
from threading import Thread
import threading
import requests
import re

BUFFER_SIZE = 1024
PATH = "/home/frost"


class ProxyServer():
    def __init__(self, ip_address="127.0.0.1", current_port=12345):
        self.current_port = current_port
        print('\n*********Server Start*********\n')
        self.proxy = socket.socket()
        self.proxy.bind((ip_address, int(current_port)))
        self.proxy.listen(10)
        self.port_regex = re.compile(
        r"(?P<type>\w{3,7}) (?P<address>(?P<https>(http://)?[?a-zA-ZB0-9.-]+/*)*):?(?P<port>\d+)? .+")
        self.all_threads = set()

    def main_loop(self):

        while True:
            client_socket, client_address = self.proxy.accept()
            thread = Thread(target=self.handle_client_connection, args=(client_socket,),daemon=True)
            self.all_threads.add(thread)

            thread.start()
            # for thr in self.all_threads:
            #     thr.join()

    def handle_client_connection(self, client_socket):
        client_data = b""
        while True:
            raw_data = client_socket.recv(BUFFER_SIZE)

            try:
                client_data +=raw_data
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
        port = 443 if re.search(self.port_regex, str(client_data)).group("port") else 80
        web_server = re.search(self.port_regex, str(client_data)).group("address")
        request_kind = re.search(self.port_regex, str(client_data)).group("type")
        return port, request_kind, web_server

    @staticmethod
    def get_http_response(web_server, client):
        try:
            client_request = requests.get(web_server)
            if client_request.status_code == 200:
                response = b"HTTP/1.1 200 OK\r\nProxy-Agent: myProxyServer\r\n\r\n"
                client.send(response)
                client.sendall(bytes(client_request.text.encode("utf-8")))
            else:
                response = b"HTTP/1.1 404 Not Found\r\nProxy-Agent: myProxyServer\r\n\r\nYour Website not Found\r\n"
                client.send(response)
        except Exception as error:
            print(error)
            return

    def get_https_response(self, web_server, port, conn):
        web_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            host_ip = socket.gethostbyname(web_server)
            web_server_socket.connect((host_ip, port))
            conn.send("HTTP/1.1 200 Connection Established\r\nProxy-Agent: myProxyServer\r\n\r\n".encode("utf-8"))
            server_thread = Thread(target=self.send_data_to_server, args=(conn, web_server_socket))
            server_thread.setDaemon(True)
            server_thread.start()

            self.send_data_to_client(conn, web_server_socket)
        except Exception as error:
            print(error)
            return

    @staticmethod
    def send_data_to_server(client_socket, server_socket: socket):
        while True:
            client_data = client_socket.recv(BUFFER_SIZE)
            server_socket.sendall(client_data)
            if len(client_data) < 1:
                break

    @staticmethod
    def send_data_to_client(client_socket, server_socket):
        while True:
            server_data = server_socket.recv(BUFFER_SIZE)
            client_socket.send(server_data)
            if len(server_data) < 1:
                break
