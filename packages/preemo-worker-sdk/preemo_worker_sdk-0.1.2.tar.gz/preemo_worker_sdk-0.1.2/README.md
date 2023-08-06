# Preemo Worker SDK

[![PyPi Version](https://img.shields.io/pypi/v/preemo-worker-sdk)](https://pypi.org/project/preemo-worker-sdk/)
[![License](https://img.shields.io/github/license/Preemo-Inc/worker-sdk)](https://github.com/Preemo-Inc/worker-sdk/blob/master/python/LICENSE)

This subrepo contains the python implementation of the Preemo Worker SDK.

## Installation

```
pip install preemo-worker-sdk
```

## Usage

### Register

In order to register a function with Preemo workers, you can decorate your functions as follows:

```python
from preemo.worker import register

@register(name="some_name", namespace="dev")
def do_something():
    ...
```

Both parameters, `name` and `namespace`, are optional. If the name isn't specified, it will default to the name of the function. If the namespace isn't specified, it will default to a global namespace.

```python
@register
def do_something():
    # registers with name do_something in the global namespace
    ...
```

## Contributing

[Contribution guidelines for this project](CONTRIBUTING.md)
