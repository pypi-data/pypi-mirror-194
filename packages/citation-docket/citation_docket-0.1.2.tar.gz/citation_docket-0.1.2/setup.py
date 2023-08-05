# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['citation_docket',
 'citation_docket.regexes',
 'citation_docket.regexes.models',
 'citation_docket.regexes.models.misc']

package_data = \
{'': ['*']}

install_requires = \
['citation_report>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'citation-docket',
    'version': '0.1.2',
    'description': 'Regex formula of Philippine Supreme Court citations in docket format, i.e. GR, AM, AC, BM.',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lawsql.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
