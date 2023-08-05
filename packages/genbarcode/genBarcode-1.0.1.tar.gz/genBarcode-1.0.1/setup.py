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
    'version': '1.0.1',
    'description': 'offline tracking number image rendering tool.',
    'long_description': "# genBarcode\n\ngenBarcode is a cli tool I created to simply take a string and generate barcode.\n\nI use an application on my phone to track numerous packages. When I get the tracking on my phone it's relatively easy to just add the tracking directly. But when it's on my computer I tend to copy the tracking number and paste it into one of the many online barcode generator sites. Sometimes these sites don't make the barcode big enough, or they use some different barcode that my phone has trouble reading.\n\nI figureed I'd just create a python tool to generate the barcode for me. This makes it so I don't have to rely on sites, or dealing with the hassle. The code uses python-barcode and supports the full gambit of formats offered by that library.\n\nAdditionally this just a fun project to improve my skills such as \n* learning more about packaging python tools\n* building wheels\n* uploading to pypi\n* building a reliable development environment\n* using poetry\n* using pipx\n\n# Installation\nI highly recommend you use `pipx` to install this, as it creates the virtualenv for you and seamlessly handles the loading of the virtual environment when running this tool. If you choose not to use `pipx`, you should create a virtualenv and possibly a wrapper script to launch this in the virtualenv.\n\n```sh\npipx install genBarcode\n```\n\n# Usage\n\nThe following is the help for the program\n```\nusage: genbarcode [-h] [-V] [-v] [-l] [-m METHOD] [-d DATA] [-t TRACKING]\n\n program description to be displayed by argparse\n    ex: python genBarcode.py\n\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -V, --version         show program's version number and exit\n  -v, --verbose\n  -l, --list-methods    Enumerate available generators and exit\n  -m METHOD, --method METHOD\n                        set the barcode generated type (default: code128)\n  -d DATA, --data DATA  Provide data to be used to generate the barcode\n  -t TRACKING, --tracking TRACKING\n                        Provide tracking number to be used to generate the barcode, stub for --data\n```\n\nOne of `-d` or `-t` is required. You can use either one.\n\n# Examples\n\n```sh\n# print help/usage\ngenBarcode -h\n\n# print all available barcode formats\ngenBarcode -l\n\n# print all available barcode formats\ngenBarcode -l\n\n# USPS sample\ngenBarcode -d 9400123456789999876500\n\n# UPS sample\ngenBarcode --data 1Z9999999999999999\n\n# Fedex sample\ngenBarcode --tracking 123456789012\n\n# Generate isbn for 1984/George.Orwell\ngenBarcode -m isbn -d 9780451524935\ngenBarcode -m isbn13 -d 9780451524935\ngenBarcode -m isbn10 -d 0451524934\n```\n\n# Credits\n\nThis package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [tbennett6421/pythoncookie](https://github.com/tbennett6421/pythoncookie) project template.\n",
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
