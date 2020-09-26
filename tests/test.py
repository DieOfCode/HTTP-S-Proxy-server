from collections import namedtuple
import unittest

from proxy_server.proxy import Proxy


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.test_proxy = Proxy()
        request = namedtuple("Request", ["body", "host", "port", "request_kind"])
        self.request_list = [
            request(body=b'GET http://static.kremlin.ru/media/events/highlight-images/index'
                         b'/ORrlAhGrykBsRNBrOnpAzt3MyXPwqhWa.jpg HTTP/1.1\r\nHost: static.kremlin.ru\r\n'
                         b'Proxy-Connection: keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) '
                         b'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36\r\n'
                         b'Accept: image/avif,image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: '
                         b'http://kremlin.ru/\r\n '
                         b'Accept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n',
                    host="http://static.kremlin.ru/media/events/highlight-images/index"
                         "/ORrlAhGrykBsRNBrOnpAzt3MyXPwqhWa.jpg",
                    port=80,
                    request_kind="GET"),
            request(body=b'CONNECT update.googleapis.com:443 HTTP/1.1\r\nHost: update.googleapis.com:443\r\n'
                         b'Proxy-Connection: keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) '
                         b'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36\r\n\r\n',
                    host="update.googleapis.com",
                    port=443,
                    request_kind="CONNECT"
                    )]

    def test_parse_request(self):
        # for element in self.request_list:
        for element in self.request_list:
            self.assertEqual((self.test_proxy.parse_data(element.body)),
                             (element.port, element.request_kind, element.host))


if __name__ == "__main__":
    unittest.main()
