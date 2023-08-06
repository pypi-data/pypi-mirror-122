from aws_cdk.aws_apigatewayv2 import CfnApi
from aws_cdk.aws_cloudfront import CachePolicy
from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from b_cfn_custom_userpool_authorizer.config.user_pool_ssm_config import UserPoolSsmConfig

from b_cfn_api_v2.api import Api
from b_cfn_api_v2_test.integration.infrastructure.authorized_endpoint_stack import AuthorizedEndpointStack
from b_cfn_api_v2_test.integration.infrastructure.user_pool_stack import UserPoolStack


class MainStack(TestingStack):
    API_ENDPOINT_KEY = 'ApiEndpoint'
    USER_POOL_ID_KEY = 'UserPoolId'
    USER_POOL_CLIENT_ID_KEY = 'UserPoolClientId'

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope)

        prefix = TestingStack.global_prefix()

        self.user_pool_stack = UserPoolStack(self)

        self.api = Api(
            scope=self,
            id='Api',
            name=f'{prefix}Api',
            description='Sample description.',
            protocol_type='HTTP',
            cors_configuration=CfnApi.CorsProperty(
                allow_methods=['GET', 'PUT', 'POST', 'OPTIONS', 'DELETE'],
                allow_origins=['*'],
                allow_headers=[
                    'Content-Type',
                    'Authorization'
                ],
                max_age=300
            )
        )

        self.api.enable_authorizer(UserPoolSsmConfig(
            user_pool_id_ssm_key=self.user_pool_stack.ssm_pool_id.parameter_name,
            user_pool_client_id_ssm_key=self.user_pool_stack.ssm_pool_client_id.parameter_name,
            user_pool_region_ssm_key=self.user_pool_stack.ssm_pool_region.parameter_name,
        ), cache_ttl=0)

        self.api.enable_default_stage('test')

        self.endpoint_stack = AuthorizedEndpointStack(self, self.api)

        self.add_output(self.API_ENDPOINT_KEY, value=f'{self.api.full_url}/dummy')
        self.add_output(self.USER_POOL_ID_KEY, value=self.user_pool_stack.pool.user_pool_id)
        self.add_output(self.USER_POOL_CLIENT_ID_KEY, value=self.user_pool_stack.client.user_pool_client_id)
