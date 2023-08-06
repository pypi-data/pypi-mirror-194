# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strtool',
 'strtool.balancerv2cad.scripts',
 'strtool.balancerv2cad.src.balancerv2cad',
 'strtool.balancerv2cad.src.balancerv2cad.logger',
 'strtool.balancerv2cad.tests',
 'strtool.balancerv2cad.tests.unit-test',
 'strtool.enums',
 'strtool.graph']

package_data = \
{'': ['*'],
 'strtool': ['abi/*',
             'balancerv2cad/.gitignore',
             'balancerv2cad/.gitignore',
             'balancerv2cad/.gitignore',
             'balancerv2cad/.gitignore',
             'balancerv2cad/README.md',
             'balancerv2cad/README.md',
             'balancerv2cad/README.md',
             'balancerv2cad/README.md',
             'balancerv2cad/notebooks/*',
             'balancerv2cad/poetry.lock',
             'balancerv2cad/poetry.lock',
             'balancerv2cad/poetry.lock',
             'balancerv2cad/poetry.lock',
             'balancerv2cad/pyproject.toml',
             'balancerv2cad/pyproject.toml',
             'balancerv2cad/pyproject.toml',
             'balancerv2cad/pyproject.toml',
             'deployments/20230117-authorizer/abi/*',
             'deployments/20230117-authorizer/output/*',
             'deployments/20230117-composable-stable-pool-v3/abi/*',
             'deployments/20230117-composable-stable-pool-v3/output/*',
             'deployments/20230117-vault/abi/*',
             'deployments/20230117-vault/output/*',
             'deployments/20230120-weighted-pool-v3/abi/*',
             'deployments/20230120-weighted-pool-v3/output/*']}

install_requires = \
['Cython==0.29.24',
 'cytoolz==0.11.2',
 'eth-abi==2.1.1',
 'gql==2.0.0',
 'jstyleson==0.0.2',
 'multicaller>=0.0.0a14',
 'requests==2.25.1',
 'web3==5.19.0']

setup_kwargs = {
    'name': 'strtool',
    'version': '0.0.0a92',
    'description': 'Streamable-finance DEX Python API',
    'long_description': 'None',
    'author': 'bernardas',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
