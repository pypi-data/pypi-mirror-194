# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ra_utils']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools==9.0.0', 'structlog==22.3.0', 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{':extra == "frozendict" or extra == "all"': ['frozendict>=2.3.4,<3.0.0'],
 ':extra == "prometheus-client" or extra == "all"': ['prometheus-client>=0.16.0,<0.17.0'],
 'all': ['Jinja2>=3.1.2,<4.0.0',
         'pydantic>=1.10.2,<2.0.0',
         'requests>=2.28.1,<3.0.0',
         'sentry-sdk>=1.12.1,<2.0.0'],
 'headers': ['pydantic>=1.10.2,<2.0.0', 'requests>=2.28.1,<3.0.0'],
 'jinja': ['Jinja2>=3.1.2,<4.0.0'],
 'pydantic': ['pydantic>=1.10.2,<2.0.0'],
 'sentry': ['pydantic>=1.10.2,<2.0.0', 'sentry-sdk>=1.12.1,<2.0.0']}

setup_kwargs = {
    'name': 'ra-utils',
    'version': '1.11.16',
    'description': 'Utilities for OS2mo/LoRa',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>\nSPDX-License-Identifier: MPL-2.0\n-->\n\n\n# RA Utils\n\nVarious code utilities for OS2mo/LoRa\n\n## License\n- This project: [MPL-2.0](MPL-2.0.txt)\n\nThis project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.\n',
    'author': 'Magenta',
    'author_email': 'info@magenta.dk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://magenta.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
