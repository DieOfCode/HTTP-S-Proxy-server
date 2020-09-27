class ProxyServerException(Exception):
    pass


class ParserException(AttributeError):
    message = "failed to process request"
