# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lineagebundle',
 'lineagebundle.json',
 'lineagebundle.lineage',
 'lineagebundle.notebook',
 'lineagebundle.notebook.NotebookParserTest_sample',
 'lineagebundle.notebook.dag',
 'lineagebundle.notebook.decorator',
 'lineagebundle.notebook.function',
 'lineagebundle.orchestration',
 'lineagebundle.pipeline',
 'lineagebundle.publish']

package_data = \
{'': ['*'],
 'lineagebundle': ['_config/*'],
 'lineagebundle.orchestration': ['templates/*'],
 'lineagebundle.publish': ['templates/*']}

install_requires = \
['SQLAlchemy>=1.3,<2.0',
 'console-bundle>=0.5,<0.6',
 'daipe-core>=1.0,<2.0',
 'minify-html>=0.6.8,<0.7.0',
 'networkx>=2.6.3,<3.0.0',
 'pyfony-bundles>=0.4.0,<0.5.0',
 'pyfony-sqlalchemy-bundle>=1.0.0,<2.0.0']

entry_points = \
{'pyfony.bundle': ['create = lineagebundle.LineageBundle:LineageBundle']}

setup_kwargs = {
    'name': 'lineage-bundle',
    'version': '1.1.0a2',
    'description': 'Lineage generation bundle',
    'long_description': '# Lineage bundle\n\n**This package is distributed under the "DataSentics SW packages Terms of Use." See [license](https://raw.githubusercontent.com/daipe-ai/lineage-bundle/master/LICENSE.txt)**\n\nLineage bundle allows you to generate and publish lineage of notebooks and notebook functions of your __Daipe__ project.\n\n## Getting started\n\n### Add _lineage-bundle_ to your project\n```yaml\npoetry add lineage-bundle --dev\n```\n\n### Generate and publish lineage to a static HTML\n```bash\nconsole lineage:publish:html\n```\n\n## Optional:\n\n#### To use a databaase: add _sqlalchemybundle.yaml_ file to `[PROJECT_NAME]/_config/bundles/`\n```yaml\nparameters:\n  sqlalchemybundle:\n    connections:\n      default:\n        engine: mssql\n        server: \'%env(DB_HOST)%\'\n        database: \'%env(DB_NAME)%\'\n        username: \'%env(DB_USER)%\'\n        password: \'%env(DB_PASS)%\'\n        driver: \'{ODBC Driver 17 for SQL Server}\'\n```\n#### In _.env_ in your Daipe project\n\n```yaml\nAPP_ENV=dev\n\n# Databricks\nDBX_TOKEN=\n# Lineage\nDB_HOST=address.of.mssql.server.com\nDB_NAME=db_name\nDB_USER=username\nDB_PASS=password\n```\n\n#### Initialize the database\n```bash\nconsole lineage:database:init\n```\n\n#### Generate and publish lineage to database\n```bash\nconsole lineage:publish:database\n```\n\n## Preview\n### Pipelines lineage\n![Example lineage](https://raw.githubusercontent.com/daipe-ai/lineage-bundle/master/static/lineage.png)\n### Functions lineage\n![Example lineage](https://raw.githubusercontent.com/daipe-ai/lineage-bundle/master/static/lineage-functions.png)\n',
    'author': 'Datasentics',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/lineage-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
