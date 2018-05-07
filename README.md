## Telepy — Python wrapper for TDLib
[![Latest Release](https://pypip.in/version/telepy/badge.svg)](https://pypi.python.org/pypi/telepy/) [![Build Status](https://travis-ci.org/Ivan-Istomin/telepy.svg?branch=master)](https://travis-ci.org/Ivan-Istomin/telepy)
Telepy is incredible, ultra-fast wrapper for [TDLib](https://core.telegram.org/tdlib), a cross-platform, fully functional Telegram client.

## How to install
Just download in from PyPi:
~~pip install telepy~~ — work in process


## How to use

```python
import sys
from telepy import Telepy

tg = Telepy()

while True:
    e = tg.td_receive()

    # If client is closed, we need to destroy it and create new client
    if e and e['@type'] is 'updateAuthorizationState' and
        e['authorization_state']['@type'] is 'authorizationStateClosed':
        
        break

    # Handle an incoming update or an answer to a previously sent request
    print(event)
    sys.stdout.flush()
```

## TODO

- [ ] Compiled TDLib on all available platforms
- [ ] Function for download library binari of TDLib for your OS
- [ ] Setuo Travis
- [ ] Add to PyPi
- [ ] Add to Conda
- [ ] Write documentation
- [ ] Write tests for complete coverage