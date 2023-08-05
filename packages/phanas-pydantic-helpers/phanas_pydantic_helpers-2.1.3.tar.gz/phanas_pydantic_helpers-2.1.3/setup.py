# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phanas_pydantic_helpers',
 'phanas_pydantic_helpers.common',
 'phanas_pydantic_helpers.fields',
 'phanas_pydantic_helpers.helpers']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'typing-extensions>=4.4.0,<5.0.0']

extras_require = \
{'time': ['pendulum>=2.1.2,<3.0.0', 'pytimeparse>=1.1.8,<2.0.0']}

setup_kwargs = {
    'name': 'phanas-pydantic-helpers',
    'version': '2.1.3',
    'description': 'A collection of helper functions/classes for Pydantic.',
    'long_description': '# Phana\'s Pydantic Helpers\n\n[![pypi](https://img.shields.io/pypi/v/phanas-pydantic-helpers)]()\n[![pypi-python](https://img.shields.io/pypi/pyversions/phanas-pydantic-helpers)]()\n[![license](https://img.shields.io/github/license/phanabani/phanas-pydantic-helpers)](LICENSE)\n\nA collection of helper functions/classes for Pydantic.\n\n## Table of Contents\n\n- [Install](#install)\n- [Usage](#usage)\n- [Changelog](#changelog)\n- [Developers](#developers)\n- [License](#license)\n\n## Install\n\n### Prerequisites\n\n- [Poetry](https://python-poetry.org/docs/#installation) – dependency manager\n\n### Install Phana\'s Pydantic Helpers\n\nTo get started, install the package with Poetry.\n\n```shell\npoetry add phanas-pydantic-helpers\n```\n\n## Usage\n\n### `Factory`\n\n`Factory(...)` is simply an alias for `pydantic.Field(default_factory=...).`\n\n```python\nfrom pydantic import BaseModel\n\nfrom phanas_pydantic_helpers import Factory\n\n\nclass Config(BaseModel):\n    token: str\n    \n    class _ExtraInfo(BaseModel):\n        name: str = "Unnamed"\n        description: str = "Empty description"\n\n    extra_info: _ExtraInfo = Factory(_ExtraInfo)\n\n\nmodel = Config(token="bleh")\nassert model.extra_info.name == "Unnamed"\nmodel.extra_info.description = "A more detailed description"\n```\n\n### `FieldConverter`\n\nEasily create custom fields with one or more type converters. Make sure the\nfirst superclass is the type you want to represent, as this is considered\nthe main base class and will take precedence over FieldConverter, offering\nbetter code completion.\n\n```python\nfrom phanas_pydantic_helpers import FieldConverter\nfrom pydantic import BaseModel\n\n\nclass ToInt(int, FieldConverter):\n\n    @classmethod\n    def _pyd_convert_str(cls, value: str) -> int:\n        return int(value)\n\n    @classmethod\n    def _pyd_convert_bytes(cls, value: bytes) -> int:\n        return int.from_bytes(value, "big")\n\n\nclass Container(BaseModel):\n    value: ToInt\n\n\ncontainer_from_str = Container(value="5")\nassert container_from_str.value == 5\n\ncontainer_from_bytes = Container(value=b"\\x00\\xFF")\nassert container_from_bytes.value == 0xFF\n```\n\n### `create_template_from_model`\n\nCreate a dict from a model with required fields. This function fills in required\nfields with placeholders.\n\n```python\nfrom typing import Dict, List\n\nfrom pydantic import BaseModel\nfrom phanas_pydantic_helpers import Factory, create_template_from_model\n\n\nclass Player(BaseModel):\n    name: str\n    admin = False\n    highest_score: float = 1.0\n    extra_data: Dict[str, str]\n\n\nclass PlayerDatabase(BaseModel):\n    version: int\n    players: List[Player]\n\n\nclass GameSystem(BaseModel):\n    system_name = "PhanaBox"\n    games: List[str]\n    player_database: PlayerDatabase = Factory(PlayerDatabase)\n\n\nassert create_template_from_model(GameSystem) == {\n    "system_name": "PhanaBox",\n    "games": ["GAMES"],\n    "player_database": {\n        "version": 0,\n        "players": [\n            {\n                "name": "NAME",\n                "admin": False,\n                "highest_score": 1.0,\n                "extra_data": {"KEY_NAME": "EXTRA_DATA"},\n            }\n        ],\n    },\n}\n```\n\n## Changelog\n\nSee [CHANGELOG.md](CHANGELOG.md).\n\n## Developers\n\n### Installation\n\nFollow the installation steps in [install](#install) and use Poetry to \ninstall the development dependencies:\n\n```shell\npoetry install\n```\n\n## License\n\n[MIT © Phanabani.](LICENSE)\n',
    'author': 'Phanabani',
    'author_email': 'phanabani@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Phanabani/phanas-pydantic-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
