# Outline API

[![PyPI version](https://badge.fury.io/py/outline-api.svg)](https://badge.fury.io/py/outline-api)

Outline API is a wrapper api written in python to access Outline VPN API services. Outline VPN APIs are used for Outline keys maintenance as well as for monitoring purposes. The package also provides wrappers to access Prometheus on the Outline VPN.

## Install

use pip to install the package:
```
pip install outline-api
```


## Using package

import the package and cerate a management object.

```python
from outline_api import (
    Manager,
    get_key_numbers, 
    get_active_keys)


apiurl = "http://127.0.0.1/apikey"
apicrt = "apicert"
manager = Manager(apiurl=apiurl, apicrt=apicrt)

new_key = manager.new()
if new_key is not None:
    print(new_key)

keys = get_key_numbers("127.0.0.1", "999")
print(keys)

active_keys = get_active_keys("127.0.0.1", "999")
print(active_keys)
```
