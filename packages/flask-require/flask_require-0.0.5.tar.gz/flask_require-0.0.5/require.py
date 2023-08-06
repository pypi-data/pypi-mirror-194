"""
Exports 2 wrappers:
- `fields`
- `admin`


## Fields
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
This ensures that any json data posted to the index contains the name field.

## Admin 

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
"""
from functools import wraps
from flask import session, request, make_response
from json import loads, dumps
import inspect


def response(name, description="", code=200):
    return make_response(
        dumps({"status": code, "name": name, "description": description}), code
    )


def fields(request, response_formatter=None, error_formatter=response, check_type=True):
    """
    Wraps the decorated function in a super function that will
    check that the required fields are present in the request
    before calling the function and passing those fields to it.
    Moreover, it will also ensure that the data passed is of the correct type.
    This only works for types that are json serializable. So if you want
    type hints for other non serializable types then you need to pass
    `check_type=False`
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get JSON data from request, if not present return 400
            default_error_response = {
                "name": "Invalid JSON",
                "description": "The request body is not valid JSON",
                "code": 400,
            }
            try:
                data = loads(request.data)
            except:
                try:
                    data = request.json
                except:
                    return error_formatter(**default_error_response)
            if data == None:
                return error_formatter(**default_error_response)

            spec = inspect.getfullargspec(func)

            if check_type:
                annotations = spec.annotations
            fields = spec.args
            args = []

            # Go through the fields and check that they all exist
            # in the JSON file. If it does not, then return a simple json
            # error
            for field in fields:
                if field in data.keys():
                    # ? The Field exists, now check type
                    if not check_type:
                        args.append(data[field])
                        continue

                    actual_type = type(data[field])
                    expected_type = annotations.get(field, actual_type)

                    if actual_type != expected_type:
                        incorrect_field_type_response = {
                            "name": "Incorrect field type",
                            "description": f"Expected '{field}' to be of type {expected_type} got type {actual_type}",
                            "code": 400,
                        }
                        return error_formatter(**incorrect_field_type_response)
                    args.append(data[field])

                else:
                    # ? The field was missing
                    missing_filed_response = {
                        "name": "Missing field",
                        "description": f"Missing field '{field}'",
                        "code": 400,
                    }
                    return error_formatter(**missing_filed_response)

            if response_formatter:
                return response_formatter(**func(*args, **kwargs))

            return func(*args, **kwargs)

        return wrapper

    return decorator


def admin(callback=None):
    """
    Wraps the decorated function in a super function that will
    check that the user is an admin before calling the function.

    This checks that the session variable contains the `admin` key
    and that the `admin` key is set to `true` for admins.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get("admin", False):
                return func(*args, **kwargs)
            else:
                if callback:
                    return callback()
                else:
                    return response(
                        "unauthorized", description="You are not an admin", code=403
                    )

        return wrapper

    return decorator
