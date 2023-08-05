# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wicked_expressions']

package_data = \
{'': ['*'], 'wicked_expressions': ['modules/*']}

install_requires = \
['beet>=0.83.1,<0.84.0',
 'bolt-expressions==0.12.2',
 'bolt>=0.29.0,<0.30.0',
 'mecha>=0.66.0,<0.67.0']

setup_kwargs = {
    'name': 'wicked-expressions',
    'version': '0.3.1',
    'description': 'Extension of bolt-expressions written in Bolt.',
    'long_description': '# wicked-expressions\n\n[![GitHub Actions](https://github.com/reapermc/wicked-expressions/workflows/CI/badge.svg)](https://github.com/reapermc/wicked-expressions/actions)\n\n> Extension of bolt-expressions written in Bolt.\n\n\n## Introduction\n\nThis is an extension of the [bolt-expressions](https://github.com/rx-modules/bolt-expressions) package. I highly recommend getting accustom to the original before using this one. This package is meant to build upon it by adding more functionality.\n\n\n```py\nfrom wicked_expressions:api import Scoreboard, Data\n\nscore_0 = Scoreboard(\'test_objective\')[\'$score_0\']\ndata_0 = Data.storage(\'my_library:internal\')[\'data_0\']\n\nscore_0 = 123\ndata_0 = 30\n\nif score_0:\n    tellraw @a "score_0 has a value"\nelse:\n    tellraw @a "score_0 has no value"\n\nif data_0 > score_0:\n    tellraw @a "data_0 is bigger than 30"\nelif data_0 == score_0:\n    tellraw @a "data_0 is equal to score_0"\n```\n\n**NOTE**: May not be fully reverse compatible with the original [bolt-expressions](https://github.com/rx-modules/bolt-expressions).\n\n\n## Installation\n\n```bash\npip install wicked_expressions\n```\n\n## Getting started\n\nThis package is designed to be used within any `bolt` script (either a `.mcfunction` or `bolt` file) inside a `bolt` enabled project.\n```yaml\nrequire:\n    - bolt\n    - wicked_expressions\n\npipeline:\n    - mecha\n```\n\nOnce you\'ve required `bolt` and `wicked-expressions`, you are able to import the python package\'s `api` module directly inside your bolt script.\n\n```py\nfrom wicked_expressions:api import Scoreboard, Data\n```\n\nNow you\'re free to use the API objects. Create simple and complex expressions, compare storages with scores, scores with scores, check if scores exist and more.\n\nCheck out the documentation [here](./docs/home.md).\n\n## Features\n\n- Most if not all the functionality of [bolt-expressions](https://github.com/rx-modules/bolt-expressions).\n- Built in score & data comparison using python\'s comparison operators.\n- Useful functions and methods especially for bolt library developers such as `.store()` and `.get()`.\n\n\n---\n\nLicense - [MIT](https://github.com/reapermc/wicked-expressions/blob/main/LICENSE)\n',
    'author': 'Yeti',
    'author_email': 'arcticyeti1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/reapermc/wicked-expressions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
