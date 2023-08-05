# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'VoiceConnectorGroupConnector',
    'VoiceConnectorOrganizationRoute',
]

@pulumi.output_type
class VoiceConnectorGroupConnector(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "voiceConnectorId":
            suggest = "voice_connector_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VoiceConnectorGroupConnector. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VoiceConnectorGroupConnector.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VoiceConnectorGroupConnector.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 priority: int,
                 voice_connector_id: str):
        """
        :param int priority: The priority associated with the Amazon Chime Voice Connector, with 1 being the highest priority. Higher priority Amazon Chime Voice Connectors are attempted first.
        :param str voice_connector_id: The Amazon Chime Voice Connector ID.
        """
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "voice_connector_id", voice_connector_id)

    @property
    @pulumi.getter
    def priority(self) -> int:
        """
        The priority associated with the Amazon Chime Voice Connector, with 1 being the highest priority. Higher priority Amazon Chime Voice Connectors are attempted first.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="voiceConnectorId")
    def voice_connector_id(self) -> str:
        """
        The Amazon Chime Voice Connector ID.
        """
        return pulumi.get(self, "voice_connector_id")


@pulumi.output_type
class VoiceConnectorOrganizationRoute(dict):
    def __init__(__self__, *,
                 host: str,
                 priority: int,
                 protocol: str,
                 weight: int,
                 port: Optional[int] = None):
        """
        :param str host: The FQDN or IP address to contact for origination traffic.
        :param int priority: The priority associated with the host, with 1 being the highest priority. Higher priority hosts are attempted first.
        :param str protocol: The protocol to use for the origination route. Encryption-enabled Amazon Chime Voice Connectors use TCP protocol by default.
        :param int weight: The weight associated with the host. If hosts are equal in priority, calls are redistributed among them based on their relative weight.
        :param int port: The designated origination route port. Defaults to `5060`.
        """
        pulumi.set(__self__, "host", host)
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "protocol", protocol)
        pulumi.set(__self__, "weight", weight)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def host(self) -> str:
        """
        The FQDN or IP address to contact for origination traffic.
        """
        return pulumi.get(self, "host")

    @property
    @pulumi.getter
    def priority(self) -> int:
        """
        The priority associated with the host, with 1 being the highest priority. Higher priority hosts are attempted first.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def protocol(self) -> str:
        """
        The protocol to use for the origination route. Encryption-enabled Amazon Chime Voice Connectors use TCP protocol by default.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter
    def weight(self) -> int:
        """
        The weight associated with the host. If hosts are equal in priority, calls are redistributed among them based on their relative weight.
        """
        return pulumi.get(self, "weight")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The designated origination route port. Defaults to `5060`.
        """
        return pulumi.get(self, "port")


