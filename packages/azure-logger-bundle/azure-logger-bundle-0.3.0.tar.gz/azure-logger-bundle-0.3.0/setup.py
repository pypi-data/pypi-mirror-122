# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['azureloggerbundle', 'azureloggerbundle.app_insights']

package_data = \
{'': ['*'], 'azureloggerbundle': ['_config/*']}

install_requires = \
['logger-bundle>=0.7.0,<0.8.0',
 'opencensus-ext-azure>=1.0,<2.0',
 'opencensus>=0.7.7,<1.0.0',
 'pyfony-bundles>=0.4.0,<0.5.0']

entry_points = \
{'pyfony.bundle': ['create = '
                   'azureloggerbundle.AzureLoggerBundle:AzureLoggerBundle']}

setup_kwargs = {
    'name': 'azure-logger-bundle',
    'version': '0.3.0',
    'description': 'Azure Logger bundle for the Pyfony framework',
    'long_description': '# Azure Logger bundle for the Pyfony Framework\n\n### Installation\n\n```bash\npoetry add azure-logger-bundle\n```\n\n### Usage\n\nGet the __instrumentation key__\n\n![instrumentation_key](docs/instrumentation_key.png)\n\nIn your project\'s `src/[ROOT_MODULE]/_config/config.yaml`\n\n```yaml\nparameters:\n  azureloggerbundle:\n    enabled: True\n    app_insights:\n      instrumentation_key: xxxx-xxxx-xxxx-xxxx\n```\n\nor use an environment variable\n\n```yaml\n      instrumentation_key: "%env(MY_SECRET_ENV)%"\n```\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/azure-logger-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
