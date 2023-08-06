# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylookyloomonitoring']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=6.1.3,<7.0.0']}

entry_points = \
{'console_scripts': ['lookyloo_monitor = pylookyloomonitoring:main']}

setup_kwargs = {
    'name': 'pylookyloomonitoring',
    'version': '0.1.0',
    'description': 'Python API to connect to lookyloo monitoring',
    'long_description': '# Python client and module for Lookyloo Monitoring\n\nThere is no public monitoring instance for now, so you will need to\ninstall [your own instance](https://github.com/Lookyloo/monitoring).\n\n## Installation\n\n```bash\npip install pylookyloomonitoring\n```\n\n## Usage\n\n### Command line\n\nYou can use the `lookyloo_monitor`:\n\n```bash\nusage: lookyloo_monitor [-h] --url URL (--monitor_url MONITOR_URL | --compare COMPARE)\n\nTalk to a Lookyloo Monitoring instance.\n\noptions:\n  -h, --help            show this help message and exit\n  --url URL             URL of the instance.\n  --monitor_url MONITOR_URL\n                        URL to monitor. It will be monitered hourly.\n  --compare COMPARE     UUID of the monitoring.\n```\n\n### Library\n\nSee [API Reference](https://pylookyloomonitoring.readthedocs.io/en/latest/api_reference.html)\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Lookyloo/PyLookylooMonitoring',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
