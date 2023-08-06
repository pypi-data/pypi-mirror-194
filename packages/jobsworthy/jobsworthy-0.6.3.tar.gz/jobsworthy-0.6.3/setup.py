# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobsworthy',
 'jobsworthy.model',
 'jobsworthy.observer',
 'jobsworthy.observer.domain',
 'jobsworthy.observer.repo',
 'jobsworthy.performance',
 'jobsworthy.performance.repo',
 'jobsworthy.repo',
 'jobsworthy.spark_job',
 'jobsworthy.structure',
 'jobsworthy.structure.puml',
 'jobsworthy.structure.puml.builder',
 'jobsworthy.structure.puml.code_generator',
 'jobsworthy.structure.puml.model',
 'jobsworthy.structure.puml.util',
 'jobsworthy.structure.puml.writer',
 'jobsworthy.util']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'azure-identity>=1.11.0,<2.0.0',
 'azure-storage-file-datalake>=12.9.1,<13.0.0',
 'click>=8.1.3,<9.0.0',
 'delta-spark>=2.1.1,<3.0.0',
 'dependency-injector>=4.40.0,<5.0.0',
 'pino>=0.6.0,<0.7.0',
 'pyspark>=3.3.0,<4.0.0',
 'rdflib>=6.2.0,<7.0.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['infra = databricker.infra:cli',
                     'puml = jobsworthy.structure.puml.cli:cli']}

setup_kwargs = {
    'name': 'jobsworthy',
    'version': '0.6.3',
    'description': '',
    'long_description': '# Jobsworth\n\n\nA set of utility functions and classes to aid in build Spark jobs on the Azure Databricks Platform.\n\n## Spark Job\n\n+ [Spark Job](docs/job/spark-job.md)\n+ Job Configuration\n\n## Util Module\n\n+ [Secrets](docs/util/secrets.md)\n+ Spark Session\n\n## Model Module\n\n+ [The Model Module](docs/model/model.md)\n\n## Repository Module\n\n+ [Database and Table](docs/repo/repository.md)\n\n## Structure Module\n\nThe Structure module provides functions for building a more abstract definition of a Hive table schema and abstractions\nfor creating table, column and cell data which can be provided as the data argument when creating a dataframe.\n\n+ [Generating Table Schemas from PUML Models Model Generation](docs/structure/puml-to-table-dsl.md)\n+ [Turning the output of a dataframe printSchema command into a PUML class diagram](docs/structure/hive-print-schema-to-puml-class-model.md)\n+ [Table Schema Definition](docs/structure/table-schema.md)\n\n\n',
    'author': 'Col Perks',
    'author_email': 'wild.fauve@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wildfauve/jobsworth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
