# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['as_you_wish']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['Sphinx==5.0.0', 'furo==2022.12.7']}

setup_kwargs = {
    'name': 'as-you-wish',
    'version': '0.1.0',
    'description': 'A simple python configuration lib.',
    'long_description': '# [As You Wish](https://www.youtube.com/watch?v=3toktnaqAyE)\nA simple python configuration library that works like Minecraft Forge\'s Config classes.\nI was fed up by the fact that the ```configparser``` library had little to no support for comments on values\nand also support for restoring configurations from a corrupted state.\nI also wanted a library that would validate that certain config values where of the correct type, so this is it.\n\n## Backends\nThe only current backend is the ```configparser``` library, but I would might add support for more,\nsuch as yaml, json, toml, etc.\n\n## Installation\nRun ```pip install as-you-wish``` to use this project.\n\n## Usage\nExample program usage:\n```python\nfrom as_you_wish import Config\n\nsettings = Config()\nsettings.define(\'service.api_key\', \'YOUR_API_KEY\', \'needed to connect to the api service\')\n\nsettings.load(\'settings.ini\')\n\nprint(f"API_KEY={settings.get(\'service.api_key\')}")\n```\n\nAlso check out the [docs](https://lochnessdragon.github.io/as-you-wish/) and [tests](https://github.com/lochnessdragon/as-you-wish/blob/main/tests/test_as_you_wish.py) for more api usage.\n\n## Contributing\nWe\'d love the help. Unfortunately we don\'t have a Contributing.md document yet, but if you find an issue/bug/feature request, feel free to submit it with a PR or under the Issues tab.\n\nThanks for checking us out! (The Kingdom of Florin 🏰 is yours.)\n',
    'author': 'Lochnessdragon',
    'author_email': '39635811+lochnessdragon@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lochnessdragon/as-you-wish',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
