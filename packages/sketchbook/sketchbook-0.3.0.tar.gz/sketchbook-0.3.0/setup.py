# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sketchbook']

package_data = \
{'': ['*']}

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata>=4.0.1,<5.0.0'],
 'aiofiles': ['aiofiles>=0.6,<0.8'],
 'curio': ['curio>=1.5,<2.0'],
 'docs': ['curio>=1.5,<2.0',
          'aiofiles>=0.6,<0.8',
          'sphinx>=4.1,<5.0',
          'sphinxcontrib-asyncio>=0.3.0,<0.4.0',
          'sphinx_rtd_theme>=1.0,<2.0',
          'sphinx-rtd-dark-mode>=1.2.4,<2.0.0'],
 'full': ['curio>=1.5,<2.0', 'aiofiles>=0.6,<0.8']}

setup_kwargs = {
    'name': 'sketchbook',
    'version': '0.3.0',
    'description': 'A template engine built for asyncio with async/await syntax support.',
    'long_description': 'Sketchbook\n==========\n.. image:: https://github.com/futursolo/sketchbook/actions/workflows/everything.yml/badge.svg\n  :target: https://github.com/futursolo/sketchbook/actions/workflows/everything.yml\n\n.. image:: https://coveralls.io/repos/github/futursolo/sketchbook/badge.svg?branch=master\n  :target: https://coveralls.io/github/futursolo/sketchbook?branch=master\n\n.. image:: https://img.shields.io/pypi/v/sketchbook\n  :target: https://pypi.org/project/sketchbook/\n\n.. image:: https://readthedocs.org/projects/sketchbook/badge/?version=latest\n  :target: https://sketchbook.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\nA template engine built with async/await syntax support for asyncio and curio.\n\nIntallation\n-----------\n.. code-block:: shell\n\n    $ pip install -U sketchbook\n\nSource Code\n-----------\n:code:`sketchbook` is open sourced under\n`Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_ and its\nsource code is hosted on `GitHub <https://github.com/futursolo/sketchbook/>`_.\n\nRequirements\n------------\n- Python 3.8.0+\n- aiofiles>=0.6,<1(Optional, used by :code:`sketchbook.AsyncSketchFinder`)\n\nAlternative Event Loop\n----------------------\nBeside the :code:`asyncio` module from the Python standard library, Sketchbook\ncan also be used with `curio <https://curio.readthedocs.io/en/latest/>`_.\n\nDocumentation\n-------------\nThe Documentation is hosted on `Read the Docs <https://sketchbook.readthedocs.io/en/latest/index.html>`_.\n\nLicense\n-------\nCopyright 2021 Kaede Hoshikawa\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': 'Kaede Hoshikawa',
    'author_email': 'futursolo@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/futursolo/sketchbook',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
