# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ReplicationConfigurationReplicationConfigurationArgs',
    'ReplicationConfigurationReplicationConfigurationRuleArgs',
    'ReplicationConfigurationReplicationConfigurationRuleDestinationArgs',
    'RepositoryEncryptionConfigurationArgs',
    'RepositoryImageScanningConfigurationArgs',
]

@pulumi.input_type
class ReplicationConfigurationReplicationConfigurationArgs:
    def __init__(__self__, *,
                 rule: pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleArgs']):
        """
        :param pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleArgs'] rule: The replication rules for a replication configuration. See Rule.
        """
        pulumi.set(__self__, "rule", rule)

    @property
    @pulumi.getter
    def rule(self) -> pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleArgs']:
        """
        The replication rules for a replication configuration. See Rule.
        """
        return pulumi.get(self, "rule")

    @rule.setter
    def rule(self, value: pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleArgs']):
        pulumi.set(self, "rule", value)


@pulumi.input_type
class ReplicationConfigurationReplicationConfigurationRuleArgs:
    def __init__(__self__, *,
                 destinations: pulumi.Input[Sequence[pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleDestinationArgs']]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleDestinationArgs']]] destinations: the details of a replication destination. See Destination.
        """
        pulumi.set(__self__, "destinations", destinations)

    @property
    @pulumi.getter
    def destinations(self) -> pulumi.Input[Sequence[pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleDestinationArgs']]]:
        """
        the details of a replication destination. See Destination.
        """
        return pulumi.get(self, "destinations")

    @destinations.setter
    def destinations(self, value: pulumi.Input[Sequence[pulumi.Input['ReplicationConfigurationReplicationConfigurationRuleDestinationArgs']]]):
        pulumi.set(self, "destinations", value)


@pulumi.input_type
class ReplicationConfigurationReplicationConfigurationRuleDestinationArgs:
    def __init__(__self__, *,
                 region: pulumi.Input[str],
                 registry_id: pulumi.Input[str]):
        """
        :param pulumi.Input[str] region: A Region to replicate to.
        :param pulumi.Input[str] registry_id: The account ID of the destination registry to replicate to.
        """
        pulumi.set(__self__, "region", region)
        pulumi.set(__self__, "registry_id", registry_id)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        """
        A Region to replicate to.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="registryId")
    def registry_id(self) -> pulumi.Input[str]:
        """
        The account ID of the destination registry to replicate to.
        """
        return pulumi.get(self, "registry_id")

    @registry_id.setter
    def registry_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "registry_id", value)


@pulumi.input_type
class RepositoryEncryptionConfigurationArgs:
    def __init__(__self__, *,
                 encryption_type: Optional[pulumi.Input[str]] = None,
                 kms_key: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] encryption_type: The encryption type to use for the repository. Valid values are `AES256` or `KMS`. Defaults to `AES256`.
        :param pulumi.Input[str] kms_key: The ARN of the KMS key to use when `encryption_type` is `KMS`. If not specified, uses the default AWS managed key for ECR.
        """
        if encryption_type is not None:
            pulumi.set(__self__, "encryption_type", encryption_type)
        if kms_key is not None:
            pulumi.set(__self__, "kms_key", kms_key)

    @property
    @pulumi.getter(name="encryptionType")
    def encryption_type(self) -> Optional[pulumi.Input[str]]:
        """
        The encryption type to use for the repository. Valid values are `AES256` or `KMS`. Defaults to `AES256`.
        """
        return pulumi.get(self, "encryption_type")

    @encryption_type.setter
    def encryption_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encryption_type", value)

    @property
    @pulumi.getter(name="kmsKey")
    def kms_key(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the KMS key to use when `encryption_type` is `KMS`. If not specified, uses the default AWS managed key for ECR.
        """
        return pulumi.get(self, "kms_key")

    @kms_key.setter
    def kms_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key", value)


@pulumi.input_type
class RepositoryImageScanningConfigurationArgs:
    def __init__(__self__, *,
                 scan_on_push: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] scan_on_push: Indicates whether images are scanned after being pushed to the repository (true) or not scanned (false).
        """
        pulumi.set(__self__, "scan_on_push", scan_on_push)

    @property
    @pulumi.getter(name="scanOnPush")
    def scan_on_push(self) -> pulumi.Input[bool]:
        """
        Indicates whether images are scanned after being pushed to the repository (true) or not scanned (false).
        """
        return pulumi.get(self, "scan_on_push")

    @scan_on_push.setter
    def scan_on_push(self, value: pulumi.Input[bool]):
        pulumi.set(self, "scan_on_push", value)


