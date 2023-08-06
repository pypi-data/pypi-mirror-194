# flask_require

This is a simple library to help you write cleaner flask code.

## Installation

```bash
pip install git+https://github.com/ivario123/flask_require
```

## Usage

```python
from flask import Flask,request
import require

app = Flask(__name__)

@app.route('/')
@require.fields(request)
def index(name):
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run()
```

### fields with optional response_formatter

```python
import flask
import require

app = flask.Flask(__name__)

def __response(name, description="", code=200):
    formatter_response = {"name": name, "description": description}

    return flask.make_response(dumps(formatter_response), code)

@app.route("/")
@fields(flask.request, response_formatter=__response)
def index(path):
    return {"name": "success", "description": "Works as it should"}

if __name__ == '__main__':
    app.run()
```

### Enforcing types

The system will check that the types provided in the signature and the types
provided by the caller are the same before passing the arguments to the function.

```python
from flask import Flask,request
import require

app = Flask(__name__)

@app.route('/')
@require.fields(request)
def index(name:str):
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run()
```

## Usage of admin

```python
from flask import Flask,request
from require import fields, admin

app = Flask(__name__)

@app.route('/')
@fields(request)
def index(name):
    return f"Hello, {name}!"

@app.route('/admin')
@admin()
def admin():
    return 'Hello, admin!'

def callback():
    print('Hello, callback!')

@app.route('/admin_with_callback')
@admin(callback)
def admin_with_callback():
    return 'Hello, admin with callback!'
```
