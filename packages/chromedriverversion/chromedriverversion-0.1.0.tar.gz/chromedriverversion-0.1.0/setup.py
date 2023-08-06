# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chromedriverversion']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.0,<22.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'chromedriverversion',
    'version': '0.1.0',
    'description': 'Python Module to Download and Extract the Appropriate Version of ChromeDriver for your installed Version of Chrome',
    'long_description': None,
    'author': 'Roby Culver',
    'author_email': 'robyculver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
