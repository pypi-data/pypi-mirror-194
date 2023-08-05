# sigdis

[![PyPI - Version](https://img.shields.io/pypi/v/sigdis.svg)](https://pypi.org/project/sigdis)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sigdis.svg)](https://pypi.org/project/sigdis)

Signal dispatcher

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Usage](#usage)

## Installation

```console
pip install sigdis
```

## License

`sigdis` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Usage

```python
from sigdis import Signal

app_started = Signal()


@app_started.connect
def do_some_actions(data, **_):
    print("DATA:", data)


app_started.send(data="test")
```

Check out `tests` for more.
