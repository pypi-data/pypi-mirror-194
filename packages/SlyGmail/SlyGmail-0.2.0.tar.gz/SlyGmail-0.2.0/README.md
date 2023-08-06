# ![sly logo](https://raw.githubusercontent.com/dunkyl/SlyMeta/main/sly%20logo%20py.svg) Sly Gmail for Python

<!-- elevator begin -->

> 🚧 **This library is an early work in progress! Breaking changes may be frequent.**

> 🐍 For Python 3.10+

## No boilerplate, *async* and *typed* Gmail access. 😋

```shell
pip install slygmail
```

This library does not have full coverage.
Currently, the following topics are supported:

* Sending emails
* Sending emails with attachments

You can directly grant user tokens using the command line, covering the whole OAuth 2 grant process.

<!-- elevator end -->

---

Example usage:

```python
import asyncio
from SlyGmail import *

async def main():
    gmail = Gmail(OAuth2('test/app.json', 'test/user.json'))

    await gmail.send('person@example.com', 'test subject', 'test body')

asyncio.run(main())
```

---

Example CLI usage for getting authorized:

```sh
# WINDOWS
py -m SlyGmail grant
# MacOS or Linux
python3 -m SlyGmail grant
```

Granting credentials requires a Google Cloud Console account and JSON file.
Please see https://docs.dunkyl.net/SlyAPI-Python/tutorial/oauth2.html for more information.
