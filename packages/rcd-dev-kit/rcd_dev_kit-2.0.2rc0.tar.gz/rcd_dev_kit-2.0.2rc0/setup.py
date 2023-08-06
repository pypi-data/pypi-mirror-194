# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rcd_dev_kit',
 'rcd_dev_kit.database_manager',
 'rcd_dev_kit.dataclass_manager',
 'rcd_dev_kit.decorator_manager',
 'rcd_dev_kit.file_manager',
 'rcd_dev_kit.pandas_manager',
 'rcd_dev_kit.sql_utils',
 'rcd_dev_kit.verification_utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.22.7,<2.0.0',
 'botocore>=1.25.7,<2.0.0',
 'connectorx>=0.3.0,<0.4.0',
 'elasticsearch>=7.0.0,<8.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'py-markdown-table>=0.3.3,<0.4.0',
 'pyspark>=3.0.0,<4.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'snowflake-connector-python[pandas]==2.7.9',
 'sqlalchemy-redshift>=0.8.11,<0.9.0',
 'sqlalchemy>=1.4,<2.0',
 'sqlparse>=0.4.2,<0.5.0',
 'statsmodels>=0.13.2,<0.14.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{'dagster': ['dagster>=1.0.16,<2.0.0',
             'dagit>=1.0.16,<2.0.0',
             'dagster-postgres==0.16.16',
             'dagster-k8s==0.16.16',
             'requests>=2.28.1,<3.0.0'],
 'docs': ['Sphinx>=5.2.3,<6.0.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7',
          'sphinx-autoapi>=2.0.0,<3.0.0'],
 'docs:python_version >= "3.8" and python_version < "4.0"': ['myst-nb>=0.17.1,<0.18.0'],
 'google': ['google>=3.0.0,<4.0.0',
            'google-api-python-client>=2.47.0,<3.0.0',
            'google-cloud-storage>=2.3.0,<3.0.0',
            'googletrans==3.0.0'],
 'py-test': ['pytest>=7.1,<8.0', 'pytest-cov>=3.0.0,<4.0.0']}

setup_kwargs = {
    'name': 'rcd-dev-kit',
    'version': '2.0.2rc0',
    'description': 'Interact with OIP ecosystem.',
    'long_description': "# rcd_dev_kit\n### Developed by Real Consulting Data\n\n## Description\nWe've developed `rcd-dev-kit` to facilitate the manipulation and interaction with the OIP ecosystem.\n\n## Installation\n```bash\npip install rcd-dev-kit\n```\n\n## Modules\nWe've divided our functions in four main modules:\n- [database_manager](./src/rcd_dev_kit/database_manager)\n    - Classes:\n        - [GcloudOperator()](./src/rcd_dev_kit/database_manager/gcloud_operator.py)\n        - MysqlOperator()\n        - ElasticsearchOperator()\n        - RedshiftOperator()\n        - SnowflakeOperator()\n        - S3Operator()\n    - Main Functions:\n        - index_json_bulk()\n        - index_json()\n        - index_json_bulk_parallel()\n        - [send_to_redshift()](./src/rcd_dev_kit/database_manager/redshift_operator.py)\n        - read_from_redshift()\n        - [send_metadata_to_redshift()](./src/rcd_dev_kit/database_manager/redshift_operator.py)\n        - find_tables_by_column_name()\n        - migrate_metadata_from_redshift()\n        - upload_raw_s3()\n        - download_raw_s3()\n        - [upload_to_gcloud()](./src/rcd_dev_kit/database_manager/gcloud_operator.py)\n        - [download_from_gcloud()](./src/rcd_dev_kit/database_manager/gcloud_operator.py)\n\n- [dataclass_manager](./src/rcd_dev_kit/dataclass_manager)\n    - Classes:\n        - RawDataFile()\n\n- [decorator_manager](./src/rcd_dev_kit/decorator_manager)\n    - Main Functions:\n        - timeit()\n        - debug()\n\n- [file_manager](./src/rcd_dev_kit/file_manager)\n    - Classes:\n        - FileOperator()\n        - [FileDownloader()](./src/rcd_dev_kit/file_manager/file_downloader.py)\n    - Main Functions:\n        - detect_path()\n        - detect_all_files()\n        - write_df_to_json_parallel()\n        - download_excel()\n        - download_csv()\n        - download_pdf()\n        - download_zip()\n\n- [pandas_manager](./src/rcd_dev_kit/pandas_manager)\n    - Main Functions:\n        - strip_all_text_column()\n        - check_na()\n        - check_duplication()\n        - check_quality_table_names()\n        - normalize_date_column()\n        - detect_aws_type()\n\n- [sql_utils](./src/rcd_dev_kit/sql_utils)\n    - Main Functions:\n        - convert_to_snowflake_syntax()\n        - correct_sql_system_variables_syntax()\n\n## Pre-requirements\nSince some of the functions deal with database connections(S3, Redshift, Snowflake, GCP, Elasticsearch, ...), we must\nbe careful to sensitive information. Thus, to use the functions correctly we must have a `.env` file following\nthe `.env.example` template.\n\n## Feedback\nAny questions or suggestions?\nPlease contact package maintainer.\n\n# python-sdk\nRefer to book https://py-pkgs.org/01-introduction for best practices\n\n# Maintainers\nThis package is using poetry for pkg management, it must be installed locally if you are maintaining the package.  \nFor developing and test the pkg locally, you must run `poetry install`.\n\n**This git repository has an automated CI/CD process** found on the git worflow: [main.yml](.github/workflows/main.yml). It means that once all modifications have been made, a Pull Request to main will trigger a serie of actions:    \n- Install Package: `poetry install`\n- Run Unitary Tests: `poetry run pytest -v tests/ --cov=rcd_dev_kit --cov-report=xml`\n- Build Package: `poetry build`\n- Publish Package in PyPI: `poetry publish`\n- Install Package from PyPI: `pip install rcd_dev_kit`\n- Send a Teams message with the new available version: Git Image `toko-bifrost/ms-teams-deploy-card@master`.\n\n## Contributing\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n`rcd_dev_kit` was created by RCD. It is licensed under the terms of the MIT license.\n\n## Credits\n`rcd_dev_kit` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).",
    'author': 'Davi FACANHA',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OpenInnovationProgram/rcd-dev-kit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
