# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['publish_sphinx_docs']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9', 'ghp-import>=0.5.5,<0.6.0']

entry_points = \
{'console_scripts': ['publish-sphinx-docs = publish_sphinx_docs:main.publish']}

setup_kwargs = {
    'name': 'publish-sphinx-docs',
    'version': '1.0.2',
    'description': 'A simple Python 3.6+ CLI to publish your Sphinx documentation to a Github Pages or Gitlab Pages repository.',
    'long_description': 'Publish Sphinx Docs\n********************\nA simple Python 3.6+ CLI to publish your Sphinx documentation to a\nGithub Pages or Gitlab Pages repository.\n\n\nInstallation\n=============\n``poetry add publish_sphinx_docs``\n\n\nUsage\n=====\nAt the command line, enter ``publish-sphinx-docs --help``.\n\n\nAuthors\n========\n- Alex Raichev (2018-12-03), maintainer\n\n\nDocumentation\n=============\nOn Github Pages `here <https://mrcagney.github.io/publish_sphinx_docs_docs/>`_ and built using this library :-)\n\n\nNotes\n=====\n- Experimental, so use at your own risk.\n\n\nChanges\n=======\n\n1.0.2, 2021-10-07\n-----------------\n- Updated dependencies.\n\n\n1.0.1, 2019-04-04\n-----------------\n- Removed sphinx-click from dependencies, because it was meant to be a development dependency.\n\n\n1.0.0, 2018-12-04\n------------------\n- First release.\n',
    'author': 'Alex Raichev',
    'author_email': 'araichev@mrcagney.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
