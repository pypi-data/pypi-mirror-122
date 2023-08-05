# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetInfrastructureConfigurationResult',
    'AwaitableGetInfrastructureConfigurationResult',
    'get_infrastructure_configuration',
    'get_infrastructure_configuration_output',
]

@pulumi.output_type
class GetInfrastructureConfigurationResult:
    """
    A collection of values returned by getInfrastructureConfiguration.
    """
    def __init__(__self__, arn=None, date_created=None, date_updated=None, description=None, id=None, instance_profile_name=None, instance_types=None, key_pair=None, loggings=None, name=None, resource_tags=None, security_group_ids=None, sns_topic_arn=None, subnet_id=None, tags=None, terminate_instance_on_failure=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if date_created and not isinstance(date_created, str):
            raise TypeError("Expected argument 'date_created' to be a str")
        pulumi.set(__self__, "date_created", date_created)
        if date_updated and not isinstance(date_updated, str):
            raise TypeError("Expected argument 'date_updated' to be a str")
        pulumi.set(__self__, "date_updated", date_updated)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_profile_name and not isinstance(instance_profile_name, str):
            raise TypeError("Expected argument 'instance_profile_name' to be a str")
        pulumi.set(__self__, "instance_profile_name", instance_profile_name)
        if instance_types and not isinstance(instance_types, list):
            raise TypeError("Expected argument 'instance_types' to be a list")
        pulumi.set(__self__, "instance_types", instance_types)
        if key_pair and not isinstance(key_pair, str):
            raise TypeError("Expected argument 'key_pair' to be a str")
        pulumi.set(__self__, "key_pair", key_pair)
        if loggings and not isinstance(loggings, list):
            raise TypeError("Expected argument 'loggings' to be a list")
        pulumi.set(__self__, "loggings", loggings)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_tags and not isinstance(resource_tags, dict):
            raise TypeError("Expected argument 'resource_tags' to be a dict")
        pulumi.set(__self__, "resource_tags", resource_tags)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if sns_topic_arn and not isinstance(sns_topic_arn, str):
            raise TypeError("Expected argument 'sns_topic_arn' to be a str")
        pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if terminate_instance_on_failure and not isinstance(terminate_instance_on_failure, bool):
            raise TypeError("Expected argument 'terminate_instance_on_failure' to be a bool")
        pulumi.set(__self__, "terminate_instance_on_failure", terminate_instance_on_failure)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="dateCreated")
    def date_created(self) -> str:
        """
        Date the infrastructure configuration was updated.
        """
        return pulumi.get(self, "date_created")

    @property
    @pulumi.getter(name="dateUpdated")
    def date_updated(self) -> str:
        return pulumi.get(self, "date_updated")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the infrastructure configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceProfileName")
    def instance_profile_name(self) -> str:
        """
        Name of the IAM Instance Profile associated with the configuration.
        """
        return pulumi.get(self, "instance_profile_name")

    @property
    @pulumi.getter(name="instanceTypes")
    def instance_types(self) -> Sequence[str]:
        """
        Set of EC2 Instance Types associated with the configuration.
        """
        return pulumi.get(self, "instance_types")

    @property
    @pulumi.getter(name="keyPair")
    def key_pair(self) -> str:
        """
        Name of the EC2 Key Pair associated with the configuration.
        """
        return pulumi.get(self, "key_pair")

    @property
    @pulumi.getter
    def loggings(self) -> Sequence['outputs.GetInfrastructureConfigurationLoggingResult']:
        """
        Nested list of logging settings.
        """
        return pulumi.get(self, "loggings")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the infrastructure configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Mapping[str, str]:
        """
        Key-value map of resource tags for the infrastructure created by the infrastructure configuration.
        """
        return pulumi.get(self, "resource_tags")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        Set of EC2 Security Group identifiers associated with the configuration.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> str:
        """
        Amazon Resource Name (ARN) of the SNS Topic associated with the configuration.
        """
        return pulumi.get(self, "sns_topic_arn")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        Identifier of the EC2 Subnet associated with the configuration.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Key-value map of resource tags for the infrastructure configuration.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="terminateInstanceOnFailure")
    def terminate_instance_on_failure(self) -> bool:
        """
        Whether instances are terminated on failure.
        """
        return pulumi.get(self, "terminate_instance_on_failure")


class AwaitableGetInfrastructureConfigurationResult(GetInfrastructureConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInfrastructureConfigurationResult(
            arn=self.arn,
            date_created=self.date_created,
            date_updated=self.date_updated,
            description=self.description,
            id=self.id,
            instance_profile_name=self.instance_profile_name,
            instance_types=self.instance_types,
            key_pair=self.key_pair,
            loggings=self.loggings,
            name=self.name,
            resource_tags=self.resource_tags,
            security_group_ids=self.security_group_ids,
            sns_topic_arn=self.sns_topic_arn,
            subnet_id=self.subnet_id,
            tags=self.tags,
            terminate_instance_on_failure=self.terminate_instance_on_failure)


def get_infrastructure_configuration(arn: Optional[str] = None,
                                     resource_tags: Optional[Mapping[str, str]] = None,
                                     tags: Optional[Mapping[str, str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInfrastructureConfigurationResult:
    """
    Provides details about an Image Builder Infrastructure Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.imagebuilder.get_infrastructure_configuration(arn="arn:aws:imagebuilder:us-west-2:aws:infrastructure-configuration/example")
    ```


    :param str arn: Amazon Resource Name (ARN) of the infrastructure configuration.
    :param Mapping[str, str] resource_tags: Key-value map of resource tags for the infrastructure created by the infrastructure configuration.
    :param Mapping[str, str] tags: Key-value map of resource tags for the infrastructure configuration.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['resourceTags'] = resource_tags
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:imagebuilder/getInfrastructureConfiguration:getInfrastructureConfiguration', __args__, opts=opts, typ=GetInfrastructureConfigurationResult).value

    return AwaitableGetInfrastructureConfigurationResult(
        arn=__ret__.arn,
        date_created=__ret__.date_created,
        date_updated=__ret__.date_updated,
        description=__ret__.description,
        id=__ret__.id,
        instance_profile_name=__ret__.instance_profile_name,
        instance_types=__ret__.instance_types,
        key_pair=__ret__.key_pair,
        loggings=__ret__.loggings,
        name=__ret__.name,
        resource_tags=__ret__.resource_tags,
        security_group_ids=__ret__.security_group_ids,
        sns_topic_arn=__ret__.sns_topic_arn,
        subnet_id=__ret__.subnet_id,
        tags=__ret__.tags,
        terminate_instance_on_failure=__ret__.terminate_instance_on_failure)


@_utilities.lift_output_func(get_infrastructure_configuration)
def get_infrastructure_configuration_output(arn: Optional[pulumi.Input[str]] = None,
                                            resource_tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                            tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInfrastructureConfigurationResult]:
    """
    Provides details about an Image Builder Infrastructure Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.imagebuilder.get_infrastructure_configuration(arn="arn:aws:imagebuilder:us-west-2:aws:infrastructure-configuration/example")
    ```


    :param str arn: Amazon Resource Name (ARN) of the infrastructure configuration.
    :param Mapping[str, str] resource_tags: Key-value map of resource tags for the infrastructure created by the infrastructure configuration.
    :param Mapping[str, str] tags: Key-value map of resource tags for the infrastructure configuration.
    """
    ...
