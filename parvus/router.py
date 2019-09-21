from .endpoint import AugmentedEndpoint
from typing import List, Tuple
import re


class Router:

    def __init__(self, routes: List[Tuple[str, AugmentedEndpoint]]):
        self.routes = [(re.compile(regex), route) for regex, route in routes]

    def get_endpoint(self, method: str, path: str) -> AugmentedEndpoint:
        for regex, endpoint in self.routes:
            if endpoint.METHOD == method and regex.match(path):
                return endpoint
        return None
