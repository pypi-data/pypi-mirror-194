# Cactus
Adapter to run an Azure Function Application with a WSGI Web Server.

#### How it works
Given the path of a folder containing a Function App, it builds a WSGI App parsing the Function settings. The app simply calls the Function main according to the route/methods settings.

#### Supported Function
This software is meant to support only Function which use binding httpTrigger as input and http as output. No other binding types. This is not an Azure emulator.

#### Function App structure
```
FunctionApp
|-- host.json
|-- function_1
|	|-- function.json
|	|-- __init__.py
|-- function_2
|	|-- function.json
|	|-- __init__.py
```

#### Installing
```
pip install pycactus
pip install pycactus[flask] # to use Flask as web framework
```

#### How to run

###### Create a file "wsgi.py"
```
from cactus.appfactory import build_app
app = build_app("YourFunctionAppFolder")
```
Or, to use Flask as web framework:
```
from cactus.flask import build_app
app = build_app("YourFunctionAppFolder")
```
###### Run it with a WSGI Web Server
```
gunicorn wsgi:app
uwsgi --http localhost:7071 --module wsgi:app
```
Checkout the [examples](https://github.com/Claudjos/cactus/tree/main/examples) for more.

#### Using Flask blueprints
```
from cactus.flask import build_blueprint

app = flask.Flask(__name__)
b = build_blueprint("myfunctionapp", "/path")
app.register_blueprint(b)
```

#### Testing
This module is tested using [Fir](https://pypi.org/project/pyfir/) WSGI client.
```
# Create a virtual environment 
python3 -m venv venv
source venv/bin/activate
# Install requirements
pip install -r requirements -r test-requirements
# Run tests with coverage
python -m pytest tests --cov=cactus
```
