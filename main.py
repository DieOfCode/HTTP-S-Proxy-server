from proxy_server.proxy_client import ProxyClient
from proxy_server.proxy import ProxyServer

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HTTP(S) Proxy server")
    parser.add_argument("--port", default=12345, type=int,dest="port", help="specify the port for proxy server")
    parser.add_argument('--host', default="127.0.0.1", type=str,dest="host", help="specify the host for proxy server")
    args = parser.parse_args()
    proxy_client = ProxyClient(host=args.host,port= args.port)
    proxy_client.create_connection()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
