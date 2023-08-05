# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['winrichnotify']

package_data = \
{'': ['*'], 'winrichnotify': ['data/*']}

install_requires = \
['pypiwin32>=223,<224']

setup_kwargs = {
    'name': 'winrichnotify',
    'version': '0.1.0',
    'description': 'An easy-to-use Python library for displaying rich notifications on Windows 10/11',
    'long_description': '# Windows Rich Notifications for Python (winrichnotify)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n\nAn easy-to-use Python library for displaying notifications for Windows 10 and Windows 11.\n\n![o7ja4 1](https://user-images.githubusercontent.com/4750998/192027245-5c2298c7-a036-4638-8f51-49cdb8c5b6ca.png)\n\n\n## Installation\n\n```\npip install winrichnotify\n```\n\n# Build Setup\n1. Install [Poetry](https://python-poetry.org/)\n2. Navigate to the root directory of the project and run ```poetry install```. This will install the dependencies for the project\n3. Run ```poetry build``` to generate built releases of the library.\n\n## Example\n\n```python\nfrom winrichnotify import WindowsNotifier\nnotifier = WindowsNotifier()\nnotifier.notify("This is an example notification!",\n                "With an example title!",\n                icon_path="custom.ico",\n                duration=10)\n\nnotifier.notify("Another notification!",\n                "With yet another title!",\n                icon_path=None,\n                duration=5,\n                threaded=True)\n\n# Wait for the threaded notification to finish\nwhile notifier.is_notification_active(): time.sleep(0.1)\n```\n\n## Contributing\n\nContributions are very welcome! To find a list of current contributors go [here](https://github.com/HarryPeach/WindowsRichNotifications/graphs/contributors)\n\n## License\nThis project is protected under the MIT license, available in the LICENSE file.',
    'author': 'Harry Peach',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HarryPeach/WindowsRichNotifications',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
