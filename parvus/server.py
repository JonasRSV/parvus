from .router import Router
import http.server
from typing import Tuple


class HTTPServer(http.server.HTTPServer):

    def __init__(self,
                 server_address: Tuple[str, int],
                 handler: http.server.BaseHTTPRequestHandler,
                 router: Router,
                 state=None):
        http.server.HTTPServer.__init__(self,
                                        server_address,
                                        handler)

        self.router = router
        self.state = state
