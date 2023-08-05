# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnus_extensions',
 'magnus_extensions.catalog.s3',
 'magnus_extensions.datastore.chunked_s3',
 'magnus_extensions.datastore.db',
 'magnus_extensions.datastore.s3',
 'magnus_extensions.executor.argo',
 'magnus_extensions.executor.kubeflow',
 'magnus_extensions.magnus_extension_template',
 'magnus_extensions.secrets.aws']

package_data = \
{'': ['*']}

install_requires = \
['magnus>=0.4.1,<0.5.0']

extras_require = \
{'aws': ['boto3'],
 'database': ['sqlalchemy'],
 'kubeflow': ['kfp>=1.8.18,<2.0.0']}

entry_points = \
{'magnus.catalog.BaseCatalog': ['s3 = '
                                'magnus_extensions.catalog.s3.implementation:S3Catalog'],
 'magnus.datastore.BaseRunLogStore': ['chunked-s3 = '
                                      'magnus_extensions.datastore.chunked_s3.implementation:ChunkedS3Store',
                                      's3 = '
                                      'magnus_extensions.datastore.s3.implementation:S3Store'],
 'magnus.executor.BaseExecutor': ['argo = '
                                  'magnus_extensions.executor.argo.implementation:ArgoExecutor',
                                  'kfp = '
                                  'magnus_extensions.executor.kubeflow.implementation:KubeFlowExecutor'],
 'magnus.integration.BaseIntegration': ['argo-catalog-file_system = '
                                        'magnus_extensions.executor.argo.integration:ArgoComputeFileSystemCatalog',
                                        'argo-run_log_store-buffered = '
                                        'magnus_extensions.executor.argo.integration:ArgoComputeBufferedRunLogStore',
                                        'argo-run_log_store-file_system = '
                                        'magnus_extensions.executor.argo.integration:ArgoComputeFileSystemRunLogStore',
                                        'kfp-catalog-file_system = '
                                        'magnus_extensions.executor.kubeflow.integration:KfPComputeFileSystemCatalog',
                                        'kfp-run_log_store-buffered = '
                                        'magnus_extensions.executor.kubeflow.integration:KfPComputeBufferedRunLogStore',
                                        'kfp-run_log_store-file_system = '
                                        'magnus_extensions.executor.kubeflow.integration:KfPComputeFileSystemRunLogStore',
                                        'local-container-catalog-s3 = '
                                        'magnus_extensions.catalog.s3.integration:LocalContainerComputeS3Catalog',
                                        'local-container-run_log_store-chunked-s3 '
                                        '= '
                                        'magnus_extensions.datastore.chunked_s3.integration:LocalContainerComputeS3Store',
                                        'local-container-run_log_store-s3 = '
                                        'magnus_extensions.datastore.s3.integration:LocalContainerComputeS3Store',
                                        'local-container-secrets-aws-secrets-manager '
                                        '= '
                                        'magnus_extensions.secrets.aws.integration:LocalContainerComputeAWSSecrets',
                                        'local-run_log_store-s3 = '
                                        'magnus_extensions.datastore.s3.integration:LocalComputeS3RunLogStore'],
 'magnus.secrets.BaseSecrets': ['aws-secrets-manager = '
                                'magnus_extensions.secrets.aws.implementation:AWSSecretsManager']}

setup_kwargs = {
    'name': 'magnus-extensions',
    'version': '0.2.0',
    'description': 'Extensions to Magnus core',
    'long_description': '# Welcome to Magnus Extensions\n\nDocumentation of the extensions are available at: https://astrazeneca.github.io/magnus-extensions/\n\nThis repository provides all the extensions to [magnus core package](https://github.com/AstraZeneca/magnus-core).\n\nMagnus provides 5 essential services:\n\n- Executor: A way to define and execute/transpile dag definition.\n- Catalog: An artifact store used to log and store data files generated during a pipeline execution.\n- Secrets Handler: A framework to handle secrets from different providers.\n- Logging: A comprehensive and automatic logging framework to capture essential information of a pipeline execution.\n- Experiment Tracking: A framework to interact with different experiment tracking tools.\n\nBelow is the table of all the available extensions to the above services:\n\n| Service     | Description                          |   Availability   |\n| :---------: | :----------------------------------: |  :-------------: |\n| **Executors**   |                                      |                  |   \n| Local       | Run the pipeline on local machine (default) |   Part of Magnus core |\n| Local Containers    | Run the pipeline on local containers | Part of Magnus core |\n| **Catalog**     |                                      |                  |\n| Do Nothing  | Provides no cataloging functionality |   Part of Magnus core |\n| File System  | Uses local file system (default) |   Part of Magnus core |\n| S3 | Uses S3 as a catalog | magnus_extension_catalog_s3 |\n| **Secrets**     |                                      |                  |\n| Do Nothing  | Provides no secrets handler (default) |   Part of Magnus core |\n| Dot Env  | Uses a file as secrets  |   Part of Magnus core |\n| Environment Variables  | Gets secrets from Environmental variables  |   Part of Magnus core |\n| **Logging**     |                                      |                  |\n|   Buffered  | Uses the run time buffer as logger (default) |   Part of Magnus core |\n| File System  | Uses a file system as run log store  |   Part of Magnus core |\n| S3 | Uses S3 to store logs | magnus_extension_datastore_s3 |\n| **Experiment Tracking**     |                                      |                  |\n|   Do Nothing  | Provides no experiment tracking (default) |   Part of Magnus core |\n',
    'author': 'Vijay Vammi',
    'author_email': 'mesanthu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
