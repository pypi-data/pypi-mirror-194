# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_engineering_pulumi_components',
 'data_engineering_pulumi_components.auth0',
 'data_engineering_pulumi_components.aws',
 'data_engineering_pulumi_components.aws.buckets',
 'data_engineering_pulumi_components.aws.cloud_trail',
 'data_engineering_pulumi_components.aws.glue',
 'data_engineering_pulumi_components.aws.lambdas',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.authorise_',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.copy',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.get_databases',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.get_fields',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.get_tables',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.move',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.notify',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.trigger_dag',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.unused_presigned_url',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.upload_',
 'data_engineering_pulumi_components.aws.lambdas.lambda_handlers.validate',
 'data_engineering_pulumi_components.aws.roles',
 'data_engineering_pulumi_components.pipelines']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.42,<2.0.0',
 'protobuf>=4.21.5,<5.0.0',
 'pulumi-auth0>=2.14.0,<3.0.0',
 'pulumi-aws>=5.25.0,<6.0.0',
 'pulumi==3.40.0']

setup_kwargs = {
    'name': 'data-engineering-pulumi-components',
    'version': '0.4.1.dev29',
    'description': 'Reusable components for use in Pulumi Python projects',
    'long_description': 'None',
    'author': 'MoJ Data Engineering Team',
    'author_email': 'data-engineering@digital.justice.gov.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
