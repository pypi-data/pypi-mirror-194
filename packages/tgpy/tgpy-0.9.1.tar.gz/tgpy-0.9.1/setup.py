# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgpy', 'tgpy._core', 'tgpy._handlers', 'tgpy.api', 'tgpy.std']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiorun>=2022.4.1,<2023.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'cryptg-anyos>=0.4.1,<0.5.0',
 'rich>=12.5.1,<13.0.0',
 'telethon-v1-24>=1.24.8,<2.0.0']

entry_points = \
{'console_scripts': ['tgpy = tgpy.main:main']}

setup_kwargs = {
    'name': 'tgpy',
    'version': '0.9.1',
    'description': 'Run Python code right in your Telegram messages',
    'long_description': '<div align="center" style="width: 50%">\n\n<h3>\n<a href="https://tgpy.tmat.me">\n<img alt="TGPy Logo" src="guide/docs/assets/TGPy.png" width=280>\n</a>\n \nRuns Python code snippets<br>within your Telegram messages\n</h3>\n\n<h6></h6>\n  \n[![PyPI - Downloads](https://img.shields.io/pypi/dm/tgpy?style=flat-square)](https://pypi.org/project/tgpy/)\n[![PyPI](https://img.shields.io/pypi/v/tgpy?style=flat-square&color=9B59B6)](https://pypi.org/project/tgpy/)\n[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/tgpy/tgpy?style=flat-square&label=docker&sort=semver&color=9B59B6)](https://hub.docker.com/r/tgpy/tgpy)\n[![Open issues](https://img.shields.io/github/issues-raw/tm-a-t/TGPy?style=flat-square)](https://github.com/tm-a-t/TGPy/issues)\n[![Docs](https://img.shields.io/website?style=flat-square&label=docs&url=https%3A%2F%2Ftgpy.tmat.me)](https://tgpy.tmat.me/)\n\n</div>\n\n<br>\n\nHere are a few examples of how people use TGPy:\n\n🧮 Run Python as an in-chat calculator\n\n🔍 Search for song lyrics within a chat\n\n🧹 Delete multiple messages with a command\n\n📊 Find out the most active members in a chat\n\n✏️ Instantly convert TeX to Unicode in messages:<br>For example, `x = \\alpha^7` becomes `x = α⁷`\n\n## About\n\nTGPy allows you to easily write and execute code snippets directly within your Telegram messages. Combine Telegram features with the full power of Python: Integrate with libraries and APIs. Create functions and TGPy modules to reuse code in the future. Set up code transformers and hooks to create custom commands and tweak Python syntax.\n\nTGPy uses Telegram API through the [Telethon](https://github.com/LonamiWebs/Telethon) library.\n\n## Quick Start\n\nPython 3.10+ required. Install TGPy and connect it to your Telegram account:\n\n```shell\n> pip install tgpy\n> tgpy\n```\n\nYou’re ready now. Send Python code to any chat, and it will run. Change your message to change the result. [Read more on installation](http://tgpy.tmat.me/installation/)\n\n## Learn\n\n[🙂 Basics Guide](https://tgpy.tmat.me/basics/code/)\n\n[😎 Extensibility Guide](https://tgpy.tmat.me/extensibility/context/)\n\n[📗 Reference](https://tgpy.tmat.me/reference/builtins/)\n\n[💬 Russian-Speaking Chat](https://t.me/tgpy_flood)\n\n\n## Demo\n\nhttps://user-images.githubusercontent.com/38432588/181266550-c4640ff1-71f2-4868-ab83-6ea3690c01b6.mp4\n\n<br>\n\n![A message processed with TGPy](guide/docs/assets/example.png)\n_Finding out the number of premium users in a chat_\n\n## Inspiration\n\nTGPy is inspired by [FTG](https://gitlab.com/friendly-telegram/friendly-telegram) and similar userbots. However, the key concept is different: TGPy is totally based on usage of code in Telegram rather than plugging extra modules. It was designed for running single-use scripts and reusing code flexibly. You can think of TGPy as a userbot for programmers.\n\n## Credits\n\nTGPy is built on [Telethon](https://github.com/LonamiWebs/Telethon), a Python library to interact with Telegram API.\n\nBasic code transformation (such as auto-return of values) is based on [meval](https://github.com/penn5/meval).\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'tmat',
    'author_email': 'a@tmat.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tm-a-t/TGPy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
