# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrapse']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['scrapse = scrapse.main:app']}

setup_kwargs = {
    'name': 'scrapse',
    'version': '0.1.2',
    'description': 'Package for downloading judgments',
    'long_description': "# ScrapSE\n\n## Package description\n\nScrapSE downloads the judgments in the desired format.  \nCurrently supported platforms: LEGGI D'ITALIA PA\n\n### Install scrapse\n```\npip3 install scrapse\n```\n\n### How to use\n\n#### Saving cookies - important\n```\nscrapse leggitalia save-cookie 'your_cokies'\n```\nThis command creates a `.txt` file containing `your_cookie`.\n\n#### Show filter values\n```\nscrapse leggitalia show\n```\nThis command shows the possible values to be assigned to sentence search filters.\n\n#### Download the judgments\nMake sure you have **saved** platform-related cookies before downloading the judgments!.\n```\nscrapse leggitalia scrap -l torino -s 'Sez. lavoro, Sez. V' -r 50\n```\nThis command creates a folder in `Users/your_username` named `sez.lavoro&sez.v_torino` containing the numbered judgments.\n\n#### For more help\n```\nscrapse --help\n```\n",
    'author': 'zaharia laurentiu jr marius',
    'author_email': 'zaharialorenzo@gmail.com',
    'maintainer': 'zaharia laurentiu jr marius',
    'maintainer_email': 'zaharialorenzo@gmail.com',
    'url': 'https://gitlab.di.unito.it/ngupp/ngupp-scrapse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
