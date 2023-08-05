# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbterd',
 'dbterd.adapters',
 'dbterd.adapters.targets',
 'dbterd.adapters.targets.dbml',
 'dbterd.adapters.targets.dbml.engine',
 'dbterd.adapters.targets.dbml.strategies',
 'dbterd.cli',
 'dbterd.helpers']

package_data = \
{'': ['*']}

modules = \
['README']
install_requires = \
['click>=8.1.3,<9.0.0',
 'dbt-artifacts-parser>=0.2.3,<0.3.0',
 'sql-metadata>=2.6.0,<3.0.0',
 'sqlparse>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['dbterd = dbterd.main:main']}

setup_kwargs = {
    'name': 'dbterd',
    'version': '0.1.1',
    'description': 'dbterd is a Command Line Interface (CLI) to convert dbt manifest.json file to diagram file',
    'long_description': '# dbterd\nCLI to generate DBML file from dbt manifest.json\n\n[![PyPI version](https://badge.fury.io/py/dbterd.svg)](https://badge.fury.io/py/dbterd)\n![python-cli](https://img.shields.io/badge/CLI-Python-FFCE3E?labelColor=14354C&logo=python&logoColor=white)\n\n```\npip install dbterd==0.1.1 --upgrade\n```\n\nVerify installed version:\n```\ndbterd --version\n```\n\n\n```bash\ndbterd -h\nUsage: dbterd [OPTIONS] COMMAND [ARGS]...\n\n  Tools for producing diagram-as-code\n\nOptions:\n  --version   Show the version and exit.\n  -h, --help  Show this message and exit.\n\nCommands:\n  debug  Inspect the hidden magics\n  run    Run the convert\n\n  Specify one of these sub-commands and you can find more help from there.\n```\n\n## Quick examine command\n```bash\n# note that no relationship test = no erd relationship\n\n# select all models in dbt_resto \ndbterd run -mp "./samples/v4-dbtresto" -o "./target"\n# select only models in dbt_resto excluding staging\ndbterd run -mp "./samples/v4-dbtresto" -o "./target" -s model.dbt_resto -ns model.dbt_resto.staging\n# select only models in schema name "mart" excluding staging\ndbterd run -mp "./samples/v4-dbtresto" -o "./target" -s schema:mart -ns model.dbt_resto.staging\n# select only models in schema full name "dbt.dbo" excluding staging\ndbterd run -mp "./samples/v4-dbtresto" -o "./target" -s schema:dbt.mart -ns model.dbt_resto.staging\n# other samples\ndbterd run -mp "./samples/v7-fivetranlog" -o "./target"\ndbterd run -mp "./samples/v7-adfacebook" -o "./target"\n```\n\n## Quick DEMO\n#### 1. Produce your manifest json\n\nIn your dbt project (I am using dbt-resto/[integration_tests](https://github.com/datnguye/dbt-resto) for demo purpose), try to build the docs:\n```bash\ndbt docs generate\n```\n    \n#### 2. Generate DBML\nCopy `manifest.json` into a specific folder, and run \n```\ndbterd run -mp "/path/to/manifest" -o "/path/to/output"\n# dbterd run -mp "./target/v4-dbtresto" -o "./target" -s model.dbt_resto -ns model.dbt_resto.staging\n```\n\nFile `./target/output.dbml` will be generated as the result\n\n#### 3. Build database docs site\nAssuming you\'re already familiar with [dbdocs](https://dbdocs.io/docs#installation)\n```\ndbdocs build "/path/to/output/output.dbml"\n# dbdocs build "./target/output.dbml"\n```\n\nYour terminal should provide the info as below:\n```bash\n√ Parsing file content\n? Project name:  poc\n‼ Password is not set for \'poc\'\n√ Done. Visit: https://dbdocs.io/datnguye/poc\n```\n\nThe site will be looks like:\n\n![screencapture-dbdocs-io-datnguye-poc-2022-12-18-22_02_28.png](https://github.com/datnguye/dbterd/blob/main/assets/images/screencapture-dbdocs-io-datnguye-poc-2022-12-18-22_02_28.png)\n\nResult after applied Model Selection:\n![screencapture-dbdocs-io-datnguye-poc-2023-02-25-10_29_32.png](https://github.com/datnguye/dbterd/blob/main/assets/images/screencapture-dbdocs-io-datnguye-poc-2023-02-25-10_29_32.png)\n\n## Decide to exclude Relationship Tests from ERD generated\nAdd `ignore_in_erd` attribute into your test\'s meta:\n```yml\nversion: 2\n\nmodels:\n  - name: your_model\n    columns:\n      - name: your_column\n        tests:\n          - relationships_test:\n              to: ref(\'your_other_model\')\n              field: your_other_column\n              meta:\n                ignore_in_erd: 1\n```',
    'author': 'Dat Nguyen',
    'author_email': 'datnguyen.it09@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/datnguye/dbterd',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
