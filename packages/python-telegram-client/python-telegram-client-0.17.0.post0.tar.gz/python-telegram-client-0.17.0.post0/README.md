# python-telegram-client

[![Build Status](https://github.com/alexander-akhmetov/python-telegram/workflows/python-telegram%20tests/badge.svg)](https://github.com/alexander-akhmetov/python-telegram/actions)
[![PyPI](https://img.shields.io/pypi/v/python-telegram.svg)](https://pypi.python.org/pypi/python-telegram)
[![DockerHub](https://img.shields.io/docker/automated/akhmetov/python-telegram.svg)](https://hub.docker.com/r/akhmetov/python-telegram/)
![Read the Docs (version)](https://img.shields.io/readthedocs/pip/stable.svg)

This is a fork of [alexander-akhmetov/python-telegram](https://github.com/alexander-akhmetov/python-telegram).
The root package is renamed from "telegram" to "teleclient" to avoid name conflict with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

## Installation

This library requires Python 3.6+ and Linux or MacOS.

```shell
pip install python-telegram-client
```

See [documentation](http://python-telegram.readthedocs.io/en/latest/#installation) for more details.

## How to use

Have a look at the [tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html) :)

Basic example:

```python
from teleclient.client import Telegram
from teleclient.text import Spoiler

tg = Telegram(
    api_id='api_id',
    api_hash='api_hash',
    phone='+31611111111',  # you can pass 'bot_token' instead
    database_encryption_key='changekey123',
    files_directory='/tmp/.tdlib_files/',
)
tg.login()

# if this is the first run, library needs to preload all chats
# otherwise the message will not be sent
result = tg.get_chats()
result.wait()

chat_id: int
result = tg.send_message(chat_id, Spoiler('Hello world!'))
# `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
# You can receive a result with the `wait` method of this object.
result.wait()
print(result.update)

tg.stop()  # you must call `stop` at the end of the script
```

More examples you can find in the [/examples/ directory](/examples/).

---

More information in the [documentation](http://python-telegram.readthedocs.io).

## Development

See [CONTRIBUTING.md](/CONTRIBUTING.md).
