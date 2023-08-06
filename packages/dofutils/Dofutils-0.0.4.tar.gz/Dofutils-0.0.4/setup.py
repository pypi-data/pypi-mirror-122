# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dofutils',
 'dofutils.encoding',
 'dofutils.maps',
 'dofutils.maps.constant',
 'dofutils.value',
 'dofutils.value.constant']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0', 'mypy>=0.910,<0.911']

entry_points = \
{'console_scripts': ['fmt = scripts:fmt',
                     'tcheck = scripts:type_check',
                     'tests = scripts:tests']}

setup_kwargs = {
    'name': 'dofutils',
    'version': '0.0.4',
    'description': 'Collection of useful things to build Dofus Retro bot or emulator',
    'long_description': '# Dofutils\nCollection of useful things to build Dofus Retro bot/emulator. \\\nWritten in Python3. Require Python >= 3.8. and [Poetry](https://python-poetry.org/).\n\n## Installation\nuse `pip install dofutils`\n\n## Developpement\nuse `poetry run tests` to launch all tests. \\\nuse `poetry run fmt` to format the project. \\\nuse `poetry run tcheck` to type check the project.\n\n## Acknowledgement\n[Vincent Quatrevieux](https://github.com/vincent4vx) : the author of the original lib\xa0\\\n[ArakneUtils](https://github.com/Arakne/ArakneUtils) : the original code\n\n## Author\n[Dysta](https://github.com/Dysta) (me)',
    'author': 'Dysta',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dysta/Dofutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
