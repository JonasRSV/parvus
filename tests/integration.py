from typing import Optional
import requests
import parvus
import multiprocessing
import time


@parvus.endpoint(method='GET', defaults=parvus.Response(headers=[('Content-type', 'text/plain')]))
def get_state(state: parvus.State, _) -> parvus.Response:
    return parvus.Response(content="".join(state), status=200)


@parvus.endpoint(method="POST", defaults=parvus.Response(content="", headers=[('Content-type', 'text/plain')]))
def update_state(state: parvus.State, message: Optional[str]) -> parvus.Response:
    if message:
        state.append(message)

    return parvus.Response(status=200)


@parvus.endpoint(method='GET')
def add_with_get(state, url_args) -> parvus.Response:
    state.append(url_args["cookie"])
    return parvus.Response(content=str(url_args))


@parvus.endpoint(method='GET')
def get_added_state(state, _) -> parvus.Response:
    return parvus.Response(content="".join(state))


def run_server_1():
    parvus.serve('0.0.0.0', 8000, [
        ("/.*", get_state),
        ("/.*", update_state)
    ], state=[])


def run_server_2():
    parvus.serve('0.0.0.0', 8000, [
        ("/state", get_added_state),
        ("/$", add_with_get)
    ], state=[])


def run_requests_1(response_queue):
    for i in range(10):
        requests.post("http://0.0.0.0:8000", data="+")

    response_queue.put(requests.get("http://0.0.0.0:8000/cookie/dough").text)


def run_requests_2(response_queue):
    for i in range(5):
        print(requests.get(f"http://0.0.0.0:8000/?cookie={i}&bookie=thaat").text)

    response_queue.put(requests.get("http://0.0.0.0:8000/state").text)

def serving_test1():
    server = multiprocessing.Process(target=run_server_1)

    response = multiprocessing.Queue()
    requester = multiprocessing.Process(target=run_requests_1, args=(response,))
    server.start()
    time.sleep(1)
    requester.start()
    time.sleep(1)

    r = response.get()

    assert r == '+' * 10, r
    print(r)

    server.terminate()
    requester.terminate()


def serving_test2():
    server = multiprocessing.Process(target=run_server_2)

    response = multiprocessing.Queue()
    requester = multiprocessing.Process(target=run_requests_2, args=(response,))
    server.start()
    time.sleep(1)
    requester.start()
    time.sleep(1)

    r = response.get()

    assert r == "01234", r
    print(r)

    server.terminate()
    requester.terminate()


if __name__ == "__main__":
    serving_test1()
    print()
    serving_test2()
