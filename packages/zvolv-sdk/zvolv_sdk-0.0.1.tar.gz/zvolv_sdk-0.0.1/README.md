# Python Zvolv SDK

The Zvolv Hyper automation platform offers several APIs to build apps. Each Zvolv API delivers part of the capabilities from the platform, so that you can pick just those that fit for your needs. This SDK offers a corresponding package for each of Zvolv’s APIs. They are small and powerful when used independently, and work seamlessly when used together, too.


[![pypi package][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Python Version][python-version]][pypi-url]

Whether you're building a custom app for your team, or integrating a third party service into your Zvolv workflows, Zvolv Developer Kit for Python allows you to leverage the flexibility of Python to get your project up and running as quickly as possible.

## Table of contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Getting started tutorial](#getting-started-tutorial)
* [Support](#support)

### Requirements

---

This library requires Python 3.6 and above.

> **Note:** You may need to use `python3` before your commands to ensure you use the correct Python path. e.g. `python3 --version`

```bash
python --version

-- or --

python3 --version
```

### Installation

We recommend using [PyPI][pypi] to install the Zvolv Developer Kit for Python.

```bash
$ pip install zvolv_sdk
```

### Getting started tutorial

---

Zvolv provide a Web API that gives you the ability to build applications that interact with Zvolv Hyper automation platform in a variety of ways. This Development Kit is a module based wrapper that makes interaction with that API easier. We have a basic example here with some of the more common uses but a full list of the available methods are available [here][api-methods]. More detailed examples can be found in [our guide](https://zvolvapi.github.io/python-zvolv-sdk/).

#### Sending an email from Zvolv

One of the most simple use-cases is sending an email from Zvolv. In our examples, we specify the channel name, however it is recommended to use the `channel_id` where possible. Also, if your app's bot user is not in a channel yet, invite the bot user before running the code snippet (or add `chat:write.public` to Bot Token Scopes for posting in any public channels).

```python
import os
from zvolv_sdk import WebClient
from zvolv_sdk.errors import ZvolvApiError

client = WebClient(token=os.environ['ZVOLV_BOT_TOKEN'])

try:
    response = client.chat_postMessage(channel='#random', text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a ZvolvApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")
```

Here we also ensure that the response back from Zvolv is a successful one and that the message is the one we sent by using the `assert` statement.

### Support

---

If you get stuck, we’re here to help. The following are the best ways to get assistance working through your issue:

Use our [Github Issue Tracker][gh-issues] for reporting bugs or requesting features.
Visit the [Zvolv Community][zvolv-community] for getting help using Slack Developer Kit for Python or just generally bond with your fellow Zvolv developers.

<!-- Markdown links -->

[pypi-image]: https://badge.fury.io/py/slack-sdk.svg
[pypi-url]: https://pypi.org/project/slack-sdk/
[python-version]: https://img.shields.io/pypi/pyversions/slack-sdk.svg
[build-image]: https://github.com/slackapi/python-slack-sdk/workflows/CI%20Build/badge.svg
[build-url]: https://github.com/slackapi/python-slack-sdk/actions?query=workflow%3A%22CI+Build%22
[codecov-image]: https://codecov.io/gh/slackapi/python-slack-sdk/branch/main/graph/badge.svg
[codecov-url]: https://codecov.io/gh/slackapi/python-slack-sdk
[contact-image]: https://img.shields.io/badge/contact-support-green.svg
[contact-url]: https://slack.com/support
[slackclientv1]: https://github.com/slackapi/python-slackclient/tree/v1
[api-methods]: https://api.slack.com/methods
[rtm-docs]: https://api.slack.com/rtm
[events-docs]: https://api.slack.com/events-api
[bolt-python]: https://github.com/slackapi/bolt-python
[pypi]: https://pypi.org/
[gh-issues]: https://github.com/zvolvapi/python-zvolv-sdk/issues
[zvolv-community]: https://zvolv.com/
[urllib]: https://docs.python.org/3/library/urllib.request.html
