# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['featurestorebundle',
 'featurestorebundle.databricks',
 'featurestorebundle.db',
 'featurestorebundle.delta',
 'featurestorebundle.entity',
 'featurestorebundle.feature',
 'featurestorebundle.feature.writer',
 'featurestorebundle.metadata',
 'featurestorebundle.notebook.decorator',
 'featurestorebundle.notebook.decorator.tests',
 'featurestorebundle.test',
 'featurestorebundle.windows']

package_data = \
{'': ['*'], 'featurestorebundle': ['_config/*']}

install_requires = \
['daipe-core>=1.0.0,<2.0.0',
 'gql>=2.0.0,<3.0.0',
 'pyfony-bundles>=0.4.0,<0.5.0']

entry_points = \
{'pyfony.bundle': ['create = '
                   'featurestorebundle.FeatureStoreBundle:FeatureStoreBundle']}

setup_kwargs = {
    'name': 'feature-store-bundle',
    'version': '1.1.1a2',
    'description': 'Feature Store for the Daipe AI Platform',
    'long_description': '# Feature Store bundle\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/feature-store-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
