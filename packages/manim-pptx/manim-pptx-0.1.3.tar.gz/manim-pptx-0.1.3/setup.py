# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_pptx']

package_data = \
{'': ['*']}

install_requires = \
['lxml', 'manim', 'python-pptx']

setup_kwargs = {
    'name': 'manim-pptx',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'RythenGlyth',
    'author_email': 'rythenglyth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
