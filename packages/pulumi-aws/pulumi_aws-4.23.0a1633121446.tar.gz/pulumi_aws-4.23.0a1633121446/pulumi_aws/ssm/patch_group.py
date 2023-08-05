# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PatchGroupArgs', 'PatchGroup']

@pulumi.input_type
class PatchGroupArgs:
    def __init__(__self__, *,
                 baseline_id: pulumi.Input[str],
                 patch_group: pulumi.Input[str]):
        """
        The set of arguments for constructing a PatchGroup resource.
        :param pulumi.Input[str] baseline_id: The ID of the patch baseline to register the patch group with.
        :param pulumi.Input[str] patch_group: The name of the patch group that should be registered with the patch baseline.
        """
        pulumi.set(__self__, "baseline_id", baseline_id)
        pulumi.set(__self__, "patch_group", patch_group)

    @property
    @pulumi.getter(name="baselineId")
    def baseline_id(self) -> pulumi.Input[str]:
        """
        The ID of the patch baseline to register the patch group with.
        """
        return pulumi.get(self, "baseline_id")

    @baseline_id.setter
    def baseline_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "baseline_id", value)

    @property
    @pulumi.getter(name="patchGroup")
    def patch_group(self) -> pulumi.Input[str]:
        """
        The name of the patch group that should be registered with the patch baseline.
        """
        return pulumi.get(self, "patch_group")

    @patch_group.setter
    def patch_group(self, value: pulumi.Input[str]):
        pulumi.set(self, "patch_group", value)


@pulumi.input_type
class _PatchGroupState:
    def __init__(__self__, *,
                 baseline_id: Optional[pulumi.Input[str]] = None,
                 patch_group: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PatchGroup resources.
        :param pulumi.Input[str] baseline_id: The ID of the patch baseline to register the patch group with.
        :param pulumi.Input[str] patch_group: The name of the patch group that should be registered with the patch baseline.
        """
        if baseline_id is not None:
            pulumi.set(__self__, "baseline_id", baseline_id)
        if patch_group is not None:
            pulumi.set(__self__, "patch_group", patch_group)

    @property
    @pulumi.getter(name="baselineId")
    def baseline_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the patch baseline to register the patch group with.
        """
        return pulumi.get(self, "baseline_id")

    @baseline_id.setter
    def baseline_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "baseline_id", value)

    @property
    @pulumi.getter(name="patchGroup")
    def patch_group(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the patch group that should be registered with the patch baseline.
        """
        return pulumi.get(self, "patch_group")

    @patch_group.setter
    def patch_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "patch_group", value)


class PatchGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 baseline_id: Optional[pulumi.Input[str]] = None,
                 patch_group: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an SSM Patch Group resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        production = aws.ssm.PatchBaseline("production", approved_patches=["KB123456"])
        patchgroup = aws.ssm.PatchGroup("patchgroup",
            baseline_id=production.id,
            patch_group="patch-group-name")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] baseline_id: The ID of the patch baseline to register the patch group with.
        :param pulumi.Input[str] patch_group: The name of the patch group that should be registered with the patch baseline.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PatchGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an SSM Patch Group resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        production = aws.ssm.PatchBaseline("production", approved_patches=["KB123456"])
        patchgroup = aws.ssm.PatchGroup("patchgroup",
            baseline_id=production.id,
            patch_group="patch-group-name")
        ```

        :param str resource_name: The name of the resource.
        :param PatchGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PatchGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 baseline_id: Optional[pulumi.Input[str]] = None,
                 patch_group: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PatchGroupArgs.__new__(PatchGroupArgs)

            if baseline_id is None and not opts.urn:
                raise TypeError("Missing required property 'baseline_id'")
            __props__.__dict__["baseline_id"] = baseline_id
            if patch_group is None and not opts.urn:
                raise TypeError("Missing required property 'patch_group'")
            __props__.__dict__["patch_group"] = patch_group
        super(PatchGroup, __self__).__init__(
            'aws:ssm/patchGroup:PatchGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            baseline_id: Optional[pulumi.Input[str]] = None,
            patch_group: Optional[pulumi.Input[str]] = None) -> 'PatchGroup':
        """
        Get an existing PatchGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] baseline_id: The ID of the patch baseline to register the patch group with.
        :param pulumi.Input[str] patch_group: The name of the patch group that should be registered with the patch baseline.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PatchGroupState.__new__(_PatchGroupState)

        __props__.__dict__["baseline_id"] = baseline_id
        __props__.__dict__["patch_group"] = patch_group
        return PatchGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="baselineId")
    def baseline_id(self) -> pulumi.Output[str]:
        """
        The ID of the patch baseline to register the patch group with.
        """
        return pulumi.get(self, "baseline_id")

    @property
    @pulumi.getter(name="patchGroup")
    def patch_group(self) -> pulumi.Output[str]:
        """
        The name of the patch group that should be registered with the patch baseline.
        """
        return pulumi.get(self, "patch_group")

