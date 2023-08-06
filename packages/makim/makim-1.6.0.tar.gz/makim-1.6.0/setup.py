# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makim']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'jinja2<3.0.3',
 'python-dotenv>=0.21.1,<0.22.0',
 'pyyaml<6.0',
 'sh>=1.14.3,<2.0.0',
 'xonsh>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['makim = makim.__main__:app']}

setup_kwargs = {
    'name': 'makim',
    'version': '1.6.0',
    'description': 'Simplify the usage of containers',
    'long_description': 'None',
    'author': 'Ivan Ogasawara',
    'author_email': 'ivan.ogasawara@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
