# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['factorio']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=17.0,<18.0']

setup_kwargs = {
    'name': 'factorio',
    'version': '0.1.0',
    'description': 'A fixtures replacement tool',
    'long_description': '===========================================================\nfactorio: A fixtures replacement tool\n===========================================================\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nInstallation instructions go here\n\nUsage\n^^^^^\n\nUsage description goes here\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _Changelog: https://github.com/spapanik/factorio/blob/main/CHANGELOG.rst\n.. _Documentation: https://factorio.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/spapanik/factorio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
