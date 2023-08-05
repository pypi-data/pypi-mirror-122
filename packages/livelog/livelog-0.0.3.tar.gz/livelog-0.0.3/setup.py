# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['livelog']

package_data = \
{'': ['*']}

install_requires = \
['colorama==0.4.4', 'watchdog==2.1.5']

setup_kwargs = {
    'name': 'livelog',
    'version': '0.0.3',
    'description': 'File logger and live reader',
    'long_description': '# livelog\n\n[![Linux](https://github.com/PabloLec/livelog/actions/workflows/linux-tests.yml/badge.svg)](https://github.com/PabloLec/livelog/actions/workflows/linux-tests.yml)[![macOS](https://github.com/PabloLec/livelog/actions/workflows/macos-tests.yml/badge.svg)](https://github.com/PabloLec/livelog/actions/workflows/macos-tests.yml)[![Windows](https://github.com/PabloLec/livelog/actions/workflows/windows-tests.yml/badge.svg)](https://github.com/PabloLec/livelog/actions/workflows/windows-tests.yml)\n',
    'author': 'PabloLec',
    'author_email': 'pablo.lecolinet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PabloLec/livelog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
