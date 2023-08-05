# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genBarcode', 'genBarcode.classes']

package_data = \
{'': ['*']}

install_requires = \
['python-barcode[images]>=0.13.1,<0.14.0']

entry_points = \
{'console_scripts': ['genBarcode = genBarcode.__main__:main']}

setup_kwargs = {
    'name': 'genbarcode',
    'version': '1.0.0',
    'description': 'offline tracking number image rendering tool.',
    'long_description': '# genBarcode\n\n# Credits\n\nThis package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tbennett6421/pythoncookie](https://github.com/tbennett6421/pythoncookie) project template.\n\nI got sick of throwing tracking numbers into websites to generate a thing for my camera to scan. So I made a thing\n',
    'author': 'Tyler Bennett',
    'author_email': 'tbennett6421@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tbennett6421/genBarcode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
