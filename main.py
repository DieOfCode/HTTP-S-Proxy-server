from proxy_server.proxy import Proxy
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Proxy server")
    parser.add_argument('-p', "--port", default=12345, dest="port")
    parser.add_argument('-ip', default="127.0.0.1", dest="ip address")
    args = parser.parse_args()
    proxy = Proxy(current_port=args.port)
    proxy.main_loop()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
