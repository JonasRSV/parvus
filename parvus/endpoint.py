from typing import Callable, Tuple, List, Optional, Union, TypeVar

State = TypeVar('State')
Request = Union[State, Optional[str]]

common_methods = {"GET", "POST"}


class Response:
    def __init__(self,
                 content: str = "",
                 status: int = 200,
                 headers: List[Tuple[str, str]] = [
                     ('Content-type', 'application/json')
                 ]):
        self.content = content
        self.status = status
        self.headers = headers


Endpoint = Callable[[Request], Response]
AugmentedEndpoint = Callable[[Request], Response]


def endpoint(method: str, defaults: Response = None) -> Callable[[Endpoint], AugmentedEndpoint]:
    if defaults is None:
        defaults = Response()

    if method not in common_methods:
        print(f"\033[31m{method} is not one of the common methods {common_methods}\033[0m")

    def augment(f: Callable[[Request], Response]) -> AugmentedEndpoint:
        def augmented_endpoint(*args, **kwargs):
            response = f(*args, **kwargs)
            if response is None:
                return defaults

            if response.content is None:
                response.content = defaults.content

            if response.status is None:
                response.status = defaults.status

            if response.headers is None:
                response.headers = defaults.headers

            return response

        augmented_endpoint.METHOD = method
        augmented_endpoint.__name__ = f.__name__

        return augmented_endpoint

    return augment


