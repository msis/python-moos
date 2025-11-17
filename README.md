python-moos
===========
python bindings for [MOOS](https://github.com/themoos/core-moos)

# Build Statuses
|OS       |Build Status|
|:--------|-----------:|
|Linux/OSX|[![Build Status](https://travis-ci.org/msis/python-moos.svg)](https://travis-ci.org/msis/python-moos)|
|Windows  |[![Build status](https://ci.appveyor.com/api/projects/status/ad0jwpij0xhikh5f?svg=true)](https://ci.appveyor.com/project/msis/python-moos)|

# Build Instructions
Clone the repository:

```
git clone https://github.com/msis/python-moos.git python-moos
```

Build and install python-moos:

```
cd python-moos
python setup.py build
python setup.py install
```

# Usage

python-moos provides two main classes for interacting with MOOS:

## pymoos.comms - Asynchronous Communications

For simple publish/subscribe communication with the MOOSDB:

```python
import pymoos

comms = pymoos.comms()

def on_connect():
    return comms.register('MY_VAR', 0)

comms.set_on_connect_callback(on_connect)
comms.run('localhost', 9000, 'my_client')
```

See `Documentation/examples/simplecomms.py` for a complete example.

## pymoos.app - MOOS Application Framework

For building full MOOS applications with structured lifecycle callbacks:

```python
import pymoos

app = pymoos.app()

def on_startup():
    app.set_app_freq(10.0)  # Hz
    return True

def on_connect_to_server():
    return app.register('MY_VAR', 0)

def iterate():
    # Main application loop
    return True

app.set_on_start_up_callback(on_startup)
app.set_on_connect_to_server_callback(on_connect_to_server)
app.set_iterate_callback(iterate)

app.run('localhost', 9000, 'my_app')
```

See `Documentation/examples/simpleapp.py` for a complete example.

