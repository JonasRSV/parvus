import http.server
from .parser import URLParser
from .endpoint import AugmentedEndpoint, Response
import sys
import traceback


class HTTPHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """..."""
        try:
            path, url_args = URLParser.parse(self.path)
        except ValueError as e:
            self.log_error(f"Unable to parse URL\n{e}")
            return HANDLER_500(self)

        endpoint = self.server.router.get_endpoint(self.command, path)

        if endpoint is None:
            return HANDLER_404(self)

        response = call(self, endpoint, url_args)

        if response is None:
            return HANDLER_500(self)

        self.send_response(response.status)
        for key, value in response.headers:
            self.send_header(key, value)

        encoded_message = response.content.encode('utf-8')

        self.send_header('Content-Length', len(encoded_message))
        self.end_headers()

        self.wfile.write(encoded_message)

    def do_POST(self):
        """..."""
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length)

        content = content.decode('utf-8')

        endpoint = self.server.router.get_endpoint(self.command, self.path)

        if endpoint is None:
            return HANDLER_404(self)

        response = call(self, endpoint, content)

        if response is None:
            return HANDLER_500(self)

        self.send_response(response.status)
        for key, value in response.headers:
            self.send_header(key, value)

        encoded_message = response.content.encode('utf-8')

        self.send_header('Content-Length', len(encoded_message))
        self.end_headers()

        self.wfile.write(encoded_message)


def HANDLER_404(handler: HTTPHandler):
    handler.send_response(404)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()

    handler.wfile.write(bytes(f"No handler for {handler.command} -- {handler.path}", "utf-8"))


def HANDLER_500(handler: HTTPHandler):
    handler.send_response(500)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()

    handler.wfile.write(bytes("Internal Server Error", "utf-8"))


def call(handler: HTTPHandler, endpoint: AugmentedEndpoint, *args) -> Response:
    response = None
    try:
        response = endpoint(handler.server.state, *args)
    except Exception as e:
        _, _, tb = sys.exc_info()
        print(f"""
    \033[31mError was thrown in endpoint {handler.command} -- {handler.path} 
    with handler {endpoint.__name__} \033[0m


    Error: {e}

                  """)
        traceback.print_tb(tb)

    return response
