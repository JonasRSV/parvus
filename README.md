# Parvus

---

A Simple wrapper of the Python standard library webserver. Feel free to open issues about any eventual bugs and I will try to resolve them.


## Getting started 
---

**Installation**

```bash
> git clone https://github.com/JonasRSV/parvus.git
> cd parvus
> python3 setup.py install
```

<br/>

***A minimal example***

```python
import parvus

@parvus.endpoint(method='GET')
def hello_world(*_):
  return parvus.Response(content='Hello World')

parvus.serve(routes=[('/.*', hello_world)])
``` 

```bash
> curl 0.0.0.0:8000
Hello World
```

<br/>

***A more demonstrative example***
```python
import parvus


@parvus.endpoint(method='GET',
                 defaults=parvus.Response(content='default content',
                                          headers=[('Content-type',
                                                    'default content type'),
                                                   ('random header key',
                                                    'random header value')],
                                          status=1337))
def a_get_method(state: "Application State", url_args: dict):
    """...."""
    print(f"Url args {url_args}")
    return parvus.Response(
        content="Content that will be used",
        headers=[('Content-type', 'text/plain')],  # headers that will be used
        status=200)  #status that will be used


@parvus.endpoint(method='POST',
                 defaults=parvus.Response(content='default content',
                                          headers=[('Content-type',
                                                    'default content type'),
                                                   ('random header key',
                                                    'random header value')],
                                          status=1337))
def a_post_method(state: "Application State", request: "Request Body as str"):
    print(f"Recieved {request}")
    return parvus.Response(
        content="Content that will be used",
        headers=[('Content-type', 'text/plain')],  # headers that will be used
        status=200)  #status that will be used


parvus.serve(host="0.0.0.0",
             port=8000,
             routes=[("/.*", a_get_method), ("/.*", a_post_method)],
             state={})
```


```bash
User view
> curl 0.0.0.0:8000
Content that will be used

Server view
Url args {}
127.0.0.1 - - [21/Sep/2019 17:40:57] "GET / HTTP/1.1" 200 -


User view
> curl -X POST 0.0.0.0:8000 -d "Hi"
Content that will be used

Server view
Recieved Hi
127.0.0.1 - - [21/Sep/2019 17:42:36] "POST / HTTP/1.1" 200 -


User view
> curl -X GET "0.0.0.0:8000?cookie=5&wokie=2"
Content that will be used

Server view
Url args {'cookie': '5', 'wokie': '2'}
127.0.0.1 - - [21/Sep/2019 17:44:26] "GET /?cookie=5&wokie=2 HTTP/1.1" 200 -
```
