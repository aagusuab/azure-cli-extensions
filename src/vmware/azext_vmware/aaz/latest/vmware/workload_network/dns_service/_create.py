# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "vmware workload-network dns-service create",
)
class Create(AAZCommand):
    """Create a DNS service by id in a private cloud workload network.

    :example: Create a DNS service by ID in a workload network.
        az vmware workload-network dns-service create --resource-group group1 --private-cloud cloud1 --dns-service dnsService1 --display-name dnsService1 --dns-service-ip 5.5.5.5 --default-dns-zone defaultDnsZone1 --fqdn-zones fqdnZone1 --log-level INFO --revision 1
    """

    _aaz_info = {
        "version": "2023-03-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.avs/privateclouds/{}/workloadnetworks/default/dnsservices/{}", "2023-03-01"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.dns_service = AAZStrArg(
            options=["-n", "--name", "--dns-service"],
            help="NSX DNS Service identifier. Generally the same as the DNS Service's display name",
            required=True,
        )
        _args_schema.private_cloud = AAZStrArg(
            options=["-c", "--private-cloud"],
            help="Name of the private cloud",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^[-\w\._]+$",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.default_dns_zone = AAZStrArg(
            options=["--default-dns-zone"],
            arg_group="Properties",
            help="Default DNS zone of the DNS Service.",
        )
        _args_schema.display_name = AAZStrArg(
            options=["--display-name"],
            arg_group="Properties",
            help="Display name of the DNS Service.",
        )
        _args_schema.dns_service_ip = AAZStrArg(
            options=["--dns-service-ip"],
            arg_group="Properties",
            help="DNS service IP of the DNS Service.",
        )
        _args_schema.fqdn_zones = AAZListArg(
            options=["--fqdn-zones"],
            arg_group="Properties",
            help="FQDN zones of the DNS Service.",
        )
        _args_schema.log_level = AAZStrArg(
            options=["--log-level"],
            arg_group="Properties",
            help="DNS Service log level.",
            enum={"DEBUG": "DEBUG", "ERROR": "ERROR", "FATAL": "FATAL", "INFO": "INFO", "WARNING": "WARNING"},
        )
        _args_schema.revision = AAZIntArg(
            options=["--revision"],
            arg_group="Properties",
            help="NSX revision number.",
        )

        fqdn_zones = cls._args_schema.fqdn_zones
        fqdn_zones.Element = AAZStrArg()
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.WorkloadNetworksCreateDnsService(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class WorkloadNetworksCreateDnsService(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AVS/privateClouds/{privateCloudName}/workloadNetworks/default/dnsServices/{dnsServiceId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "dnsServiceId", self.ctx.args.dns_service,
                    required=True,
                ),
                **self.serialize_url_param(
                    "privateCloudName", self.ctx.args.private_cloud,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-03-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType,
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("defaultDnsZone", AAZStrType, ".default_dns_zone")
                properties.set_prop("displayName", AAZStrType, ".display_name")
                properties.set_prop("dnsServiceIp", AAZStrType, ".dns_service_ip")
                properties.set_prop("fqdnZones", AAZListType, ".fqdn_zones")
                properties.set_prop("logLevel", AAZStrType, ".log_level")
                properties.set_prop("revision", AAZIntType, ".revision")

            fqdn_zones = _builder.get(".properties.fqdnZones")
            if fqdn_zones is not None:
                fqdn_zones.set_elements(AAZStrType, ".")

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()

            _schema_on_200_201 = cls._schema_on_200_201
            _schema_on_200_201.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _schema_on_200_201.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200_201.properties
            properties.default_dns_zone = AAZStrType(
                serialized_name="defaultDnsZone",
            )
            properties.display_name = AAZStrType(
                serialized_name="displayName",
            )
            properties.dns_service_ip = AAZStrType(
                serialized_name="dnsServiceIp",
            )
            properties.fqdn_zones = AAZListType(
                serialized_name="fqdnZones",
            )
            properties.log_level = AAZStrType(
                serialized_name="logLevel",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.revision = AAZIntType()
            properties.status = AAZStrType(
                flags={"read_only": True},
            )

            fqdn_zones = cls._schema_on_200_201.properties.fqdn_zones
            fqdn_zones.Element = AAZStrType()

            return cls._schema_on_200_201


class _CreateHelper:
    """Helper class for Create"""


__all__ = ["Create"]