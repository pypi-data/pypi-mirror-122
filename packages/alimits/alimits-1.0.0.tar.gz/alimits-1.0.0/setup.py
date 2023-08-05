# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alimits', 'alimits.storage']

package_data = \
{'': ['*']}

install_requires = \
['limits>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'alimits',
    'version': '1.0.0',
    'description': 'Provides asyncio storage and strategy implementations for the limits library.',
    'long_description': '# alimits\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/thearchitector/alimits/CI?label=tests&style=flat-square)\n![GitHub](https://img.shields.io/github/license/thearchitector/alimits?style=flat-square)\n[![Buy a tree](https://img.shields.io/badge/Treeware-%F0%9F%8C%B3-lightgreen?style=flat-square)](https://ecologi.com/eliasgabriel?r=6128126916bfab8bd051026c)\n\nProvides asyncio-compatible implementations of the [`limits` library](https://limits.readthedocs.io/en/stable/) storage and strategy options.\nUsed in the [`slowapi` library](https://slowapi.readthedocs.io/en/latest/).\n\nDocumentation is available [here](https://thearchitector.github.io/alimits/).\n\nAvailable on PyPi at [alimits](https://pypi.org/project/alimits/).\n\n## Strategies\n\nThis library implements a couple asyncio limiting strategies:\n\n- Fixed window → (`alimits.strategies.AsyncFixedWindowRateLimiter`)\n- Moving window → (`alimits.strategies.AsyncMovingWindowRateLimiter`)\n- Fixed window with elastic expiration → (`alimits.strategies.AsyncFixedWindowElasticRateLimiter`)\n\n#### Resources\n\n1. <https://limits.readthedocs.io/en/stable/strategies.html>\n2. <https://medium.com/figma-design/an-alternative-approach-to-rate-limiting-f8a06cf7c94c>\n3. <https://cloud.google.com/architecture/rate-limiting-strategies-techniques>\n\n## Storage Backends\n\nEach of the above rate limiters support a couple different storage backends:\n\n- Memory (in-memory, volatile) → (`alimits.storage.AsyncMemoryStorage`)\n- Redis (on-disk or in-memory, persistent) → (`alimits.storage.AsyncRedisStorage`)\n\nOther storage backends are a WIP.\n\n## License\n\nCopyright (c) 2021 Elias Gabriel, 2020 Laurent Savaete, 2015 Ali-Akber Saifee \n\nThis software is licensed under the [MIT License](LICENSE).\n\n---\n\nThis package is [Treeware](https://treeware.earth). If you use it in production, then we ask that you [**buy the world a tree**](https://ecologi.com/eliasgabriel?r=6128126916bfab8bd051026c) to thank us for our work. By contributing to the forest you’ll be creating employment for local families and restoring wildlife habitats.\n',
    'author': 'Elias Gabriel',
    'author_email': 'me@eliasfgabriel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thearchitector/alimits',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
