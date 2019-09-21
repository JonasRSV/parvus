from typing import List, Tuple
from .endpoint import AugmentedEndpoint, State
from .server import HTTPServer
from .handler import HTTPHandler
from .router import Router


def serve(host: str = "0.0.0.0",
          port: int = 8000,
          routes=None,
          state=None):
    """Serve 
    
    :arg host - Host name
    :arg port - Port to connect to
    :arg routes - Paths & Handlers
    :arg state - Application state
    """

    if routes is None:
        routes = []
    if state is None:
        state = {}
    with HTTPServer((host, port), HTTPHandler, router=Router(routes), state=state) as server:
        server.serve_forever()

