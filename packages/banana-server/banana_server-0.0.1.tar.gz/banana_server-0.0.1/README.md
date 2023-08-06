# server

An HTTP server designed for AI

### Quickstart

Install the Banana server package

```bash
pip3 install banana-server
```

Create a python file called `main.py` with this:

```python
from banana_server import Banana

app = Banana("server")

@app.init
def init():
    model = "my pytorch model"
    app.optimize(model)

    return app.set_cache({
        "model": model,
        "hello": "world"
    })

@app.handler
def handler(cache, json_in) -> dict:
    print("cache:", cache)
    print("json_in:", json_in)
    return {"json": "out"}

app.serve()
```

Run it with

```bash
python3 main.py
```

Test the running server with

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"test"}' http://localhost:8000
```

# Documentation

### banana_server.Banana

```python
from banana_server import Banana

app = Banana("server")
```

This instantiates your HTTP app, similar to popular frameworks like [Flask](https://flask.palletsprojects.com/en/2.2.x/_)

This HTTP server is production-ready out of the box.

### @app.init

```python
@app.init
def init():
    model = "my pytorch model"
    app.optimize(model)

    return app.set_cache({
        "model": model,
        "hello": "world"
    })
```

The `@app.init` decorated function runs once on server startup, and is used to load any reuseable, heavy objects such as:

- Your AI model, loaded to GPU
- Tokenizers
- Precalculated embeddings

Once initialized, you must save those variables to the cache with `app.set_cache({})` so they can be referenced later.

There may only be one `@app.init` function.

### @app.handler

```python
@app.handler
def handler(cache, json_in) -> dict:
    print("cache:", cache)
    print("json_in:", json_in)
    return {"json": "out"}
```

The `@app.handler` decorated function runs for every http call, and is used to run inference or training workloads against your model(s).

| Arg     | Type | Description                                                                                       |
| ------- | ---- | ------------------------------------------------------------------------------------------------- |
| cache   | dict | The app's cache, set with set_cache()                                                             |
| json_in | dict | The json body of the input call. If using the Banana client SDK, this is the same as model_inputs |

| Return Val | Type | Description                                                                                              |
| ---------- | ---- | -------------------------------------------------------------------------------------------------------- |
| json_out   | dict | The json body to return to the client. If using the Banana client SDK, this is the same as model_outputs |

There may only be one `@app.handler` function.

### app.set_cache()

```python
app.set_cache({})
```

`app.set_cache` saves the input dictionary to the app's cache, for reuse in future calls. It may be used in both the `@app.init` and `@app.handler` functions.

`app.set_cache` overwrites any preexisting cache.

### app.get_cache()

```python
cache = app.get_cache()
```

`app.get_cache` fetches the dictionary to the app's cache. This value is automatically provided for you as the `cache` argument in the `@app.handler` function.

### app.optimize(model)

```python
model # some pytorch model
app.optimize(model)
```

`app.optimize` is a feature specific to users hosting on [Banana's serverless GPU infrastructure](https://banana.dev). It is run during buildtime rather than runtime, and is used to locate the model(s) to be targeted for Banana's Fastboot optimization.

Multiple models may be optimized. Only Pytorch models are currently supported.
