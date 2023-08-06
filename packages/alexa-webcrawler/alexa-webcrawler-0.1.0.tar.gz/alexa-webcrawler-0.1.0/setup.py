# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alexa_webcrawler']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['alexa-webcrawler = alexa_webcrawler.main:app']}

setup_kwargs = {
    'name': 'alexa-webcrawler',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Alexa Webcrawler\n\nA CLI tool to show top website in different country from Alexa\n',
    'author': 'Jonathan Liew',
    'author_email': 'jonathan200934@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
