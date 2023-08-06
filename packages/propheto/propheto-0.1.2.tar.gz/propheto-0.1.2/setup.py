# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['propheto',
 'propheto.deployments',
 'propheto.deployments.aws',
 'propheto.deployments.azure',
 'propheto.deployments.gcp',
 'propheto.model_frameworks',
 'propheto.package',
 'propheto.package.templates.api',
 'propheto.package.templates.api.v1',
 'propheto.package.templates.api.v1.endpoints',
 'propheto.project',
 'propheto.project.configuration',
 'propheto.tracking']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.105,<2.0.0',
 'cloudpickle>=1.6.0,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.61.1,<5.0.0',
 'troposphere>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'propheto',
    'version': '0.1.2',
    'description': 'Propheto - MLOps Software Platform',
    'long_description': 'Propheto\n========\n\nMLOps software tooling for cloud environments.\n\n',
    'author': 'Dan McDade',
    'author_email': 'dan@propheto.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Propheto-io/propheto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
