# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import os
import unittest  # pylint: disable=unused-import

from azure.cli.testsdk import (ResourceGroupPreparer)
from azure.cli.testsdk.decorators import serial_test
from azext_containerapp.tests.latest.common import (
    ContainerappComposePreviewScenarioTest,  # pylint: disable=unused-import
    write_test_file,
    clean_up_test_file,
    TEST_DIR, TEST_LOCATION)
from .utils import prepare_containerapp_env_for_app_e2e_tests


class ContainerappComposePreviewIngressScenarioTest(ContainerappComposePreviewScenarioTest):
    @serial_test()
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_ingress_external(self, resource_group):
        self.cmd('configure --defaults location={}'.format(TEST_LOCATION))
        app = self.create_random_name(prefix='composeingress', length=24)
        compose_text = f"""
services:
  {app}:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    ports: 8080:80
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        write_test_file(compose_file_name, compose_text)

        env_id = prepare_containerapp_env_for_app_e2e_tests(self)
        self.kwargs.update({
            'environment': env_id,
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        self.cmd(command_string, checks=[
            self.check(f'[?name==`{app}`].properties.configuration.ingress.targetPort', [80]),
            self.check(f'[?name==`{app}`].properties.configuration.ingress.external', [True]),
        ])

        clean_up_test_file(compose_file_name)


class ContainerappComposePreviewIngressInternalScenarioTest(ContainerappComposePreviewScenarioTest):
    @serial_test()
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_ingress_internal(self, resource_group):
        app = self.create_random_name(prefix='composeingress', length=24)
        compose_text = f"""
services:
  {app}:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    expose:
      - "3000"
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        write_test_file(compose_file_name, compose_text)
        env_id = prepare_containerapp_env_for_app_e2e_tests(self)
        self.kwargs.update({
            'environment': env_id,
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        self.cmd(command_string, checks=[
            self.check(f'[?name==`{app}`].properties.configuration.ingress.targetPort', [3000]),
            self.check(f'[?name==`{app}`].properties.configuration.ingress.external', [False]),
        ])

        clean_up_test_file(compose_file_name)


class ContainerappComposePreviewIngressBothScenarioTest(ContainerappComposePreviewScenarioTest):
    @serial_test()
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_ingress_both(self, resource_group):
        self.cmd('configure --defaults location={}'.format(TEST_LOCATION))
        app = self.create_random_name(prefix='composeingress', length=24)
        compose_text = f"""
services:
  {app}:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    ports: 4000:3000
    expose:
      - "5000"
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        write_test_file(compose_file_name, compose_text)
        env_id = prepare_containerapp_env_for_app_e2e_tests(self)
        self.kwargs.update({
            'environment': env_id,
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        self.cmd(command_string, checks=[
            self.check(f'[?name==`{app}`].properties.configuration.ingress.targetPort', [3000]),
            self.check(f'[?name==`{app}`].properties.configuration.ingress.external', [True]),
        ])

        clean_up_test_file(compose_file_name)


class ContainerappComposePreviewIngressPromptScenarioTest(ContainerappComposePreviewScenarioTest):
    @serial_test()
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_ingress_prompt(self, resource_group):
        self.cmd('configure --defaults location={}'.format(TEST_LOCATION))
        app = self.create_random_name(prefix='composeingress', length=24)
        compose_text = f"""
services:
  {app}:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    ports:
      - 4000:3000
      - 443:443
      - 80:80
    expose:
      - "5000"
      - "3000"
      - "443"
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        write_test_file(compose_file_name, compose_text)
        env_id = prepare_containerapp_env_for_app_e2e_tests(self)
        self.kwargs.update({
            'environment': env_id,
            'compose': compose_file_name,
        })
        
        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'

        # This test fails because prompts are not supported in NoTTY environments
        self.cmd(command_string, expect_failure=True)

        clean_up_test_file(compose_file_name)
