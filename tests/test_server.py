import unittest
from proxy_server.proxy_client import ProxyClient
from proxy_server.proxy import ProxyServer
import socket


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_client_host(self):
        self.test_client = ProxyClient("666.666.666.666", 12345)

        self.assertEqual(self.test_client.host, "127.0.0.1")
