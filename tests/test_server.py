import unittest
from proxy_server.proxy_client import ProxyClient
from proxy_server.proxy import ProxyServer
import socket


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self.test_client = ProxyClient("666.666.666.666", 12345)
        self.user_socket = socket.socket()
        self.user_socket.connect(("localhost", 12345))

    def test_client_host(self):

        self.assertEqual(self.test_client.host, "127.0.0.1")

    def test_get_request(self):
        get_request = b'GET http://kremlin.ru/ HTTP/1.1\r\nHost: kremlin.ru\r\nProxy-Connection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n'
        self.user_socket.send(get_request)
        self.data = b""
        while True:
            self.data = self.user_socket.recv(1024)
            break
        self.assertEqual(b'HTTP/1.1 200 OK\r\nProxy-Agent: myProxyServer\r\n\r\n',self.data)

    def test_connect_request(self):
        get_request = b'CONNECT vk.com:443 HTTP/1.1\r\nHost: vk.com:443\r\nProxy-Connection: ' \
                      b'keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, ' \
                      b'like Gecko) Chrome/85.0.4183.102 Safari/537.36\r\n\r\n '

        self.user_socket.send(get_request)
        self.data = b""
        while True:
            self.data = self.user_socket.recv(1024)
            break
        self.assertEqual("HTTP/1.1 200 Connection Established\r\nProxy-Agent: myProxyServer\r\n\r\n".encode("utf-8"), self.data)



