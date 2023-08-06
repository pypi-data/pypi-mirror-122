# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cute_sway_recorder']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.0.0,<7.0.0']

entry_points = \
{'console_scripts': ['cute-sway-recorder = cute_sway_recorder.main:main']}

setup_kwargs = {
    'name': 'cute-sway-recorder',
    'version': '0.1.1',
    'description': 'A small graphical screen recorder for wl-roots, leveraging wf-recorder and slurp',
    'long_description': None,
    'author': 'Maor Kadosh',
    'author_email': 'pypi@avocadosh.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/it-is-wednesday/cute-sway-recorder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
