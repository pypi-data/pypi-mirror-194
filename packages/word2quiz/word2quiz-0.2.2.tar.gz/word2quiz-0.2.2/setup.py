# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['word2quiz']

package_data = \
{'': ['*'], 'word2quiz': ['locales/en/LC_MESSAGES/*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'attrs>=22.1.0,<23.0.0',
 'canvasapi>=3.0.0,<4.0.0',
 'canvasrobot',
 'docx2python>=2.0.4,<3.0.0',
 'keyring>=23.6.0,<24.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.4.4,<13.0.0']

setup_kwargs = {
    'name': 'word2quiz',
    'version': '0.2.2',
    'description': 'Create quizzes in Canvas from simple Word docx files using CanvasRobot/Canvasapi',
    'long_description': '# Word2Quiz\nCreate quizzes in Canvas from a Word docx file with defined paragraph and \ntext formatting (H1, H2, numbered lists for the question,\nalphabetic lists for the answers) using\n[Canvasapi](https://canvasapi.readthedocs.io/en/stable/getting-started.html) with the\nCanvasRobot library.\n\nA library to use in a webapp, command-line tool or gui program. \nAs an example a simple standalone command-line tool is provided.\n\n\n',
    'author': 'Nico de Groot',
    'author_email': 'ndegroot0@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ndegroot/word2quiz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
