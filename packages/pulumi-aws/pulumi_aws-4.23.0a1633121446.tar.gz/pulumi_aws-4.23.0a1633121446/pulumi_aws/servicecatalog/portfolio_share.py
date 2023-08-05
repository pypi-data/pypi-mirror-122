# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PortfolioShareArgs', 'PortfolioShare']

@pulumi.input_type
class PortfolioShareArgs:
    def __init__(__self__, *,
                 portfolio_id: pulumi.Input[str],
                 principal_id: pulumi.Input[str],
                 type: pulumi.Input[str],
                 accept_language: Optional[pulumi.Input[str]] = None,
                 share_tag_options: Optional[pulumi.Input[bool]] = None,
                 wait_for_acceptance: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a PortfolioShare resource.
        :param pulumi.Input[str] portfolio_id: Portfolio identifier.
        :param pulumi.Input[str] principal_id: Identifier of the principal with whom you will share the portfolio. Valid values AWS account IDs and ARNs of AWS Organizations and organizational units.
        :param pulumi.Input[str] type: Type of portfolio share. Valid values are `ACCOUNT` (an external account), `ORGANIZATION` (a share to every account in an organization), `ORGANIZATIONAL_UNIT`, `ORGANIZATION_MEMBER_ACCOUNT` (a share to an account in an organization).
        :param pulumi.Input[str] accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
        :param pulumi.Input[bool] share_tag_options: Whether to enable sharing of `servicecatalog.TagOption` resources when creating the portfolio share.
        :param pulumi.Input[bool] wait_for_acceptance: Whether to wait (up to the timeout) for the share to be accepted. Organizational shares are automatically accepted.
        """
        pulumi.set(__self__, "portfolio_id", portfolio_id)
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "type", type)
        if accept_language is not None:
            pulumi.set(__self__, "accept_language", accept_language)
        if share_tag_options is not None:
            pulumi.set(__self__, "share_tag_options", share_tag_options)
        if wait_for_acceptance is not None:
            pulumi.set(__self__, "wait_for_acceptance", wait_for_acceptance)

    @property
    @pulumi.getter(name="portfolioId")
    def portfolio_id(self) -> pulumi.Input[str]:
        """
        Portfolio identifier.
        """
        return pulumi.get(self, "portfolio_id")

    @portfolio_id.setter
    def portfolio_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "portfolio_id", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Input[str]:
        """
        Identifier of the principal with whom you will share the portfolio. Valid values AWS account IDs and ARNs of AWS Organizations and organizational units.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of portfolio share. Valid values are `ACCOUNT` (an external account), `ORGANIZATION` (a share to every account in an organization), `ORGANIZATIONAL_UNIT`, `ORGANIZATION_MEMBER_ACCOUNT` (a share to an account in an organization).
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[pulumi.Input[str]]:
        """
        Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
        """
        return pulumi.get(self, "accept_language")

    @accept_language.setter
    def accept_language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accept_language", value)

    @property
    @pulumi.getter(name="shareTagOptions")
    def share_tag_options(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable sharing of `servicecatalog.TagOption` resources when creating the portfolio share.
        """
        return pulumi.get(self, "share_tag_options")

    @share_tag_options.setter
    def share_tag_options(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "share_tag_options", value)

    @property
    @pulumi.getter(name="waitForAcceptance")
    def wait_for_acceptance(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to wait (up to the timeout) for the share to be accepted. Organizational shares are automatically accepted.
        """
        return pulumi.get(self, "wait_for_acceptance")

    @wait_for_acceptance.setter
    def wait_for_acceptance(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_for_acceptance", value)


@pulumi.input_type
class _PortfolioShareState:
    def __init__(__self__, *,
                 accept_language: Optional[pulumi.Input[str]] = None,
                 accepted: Optional[pulumi.Input[bool]] = None,
                 portfolio_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 share_tag_options: Optional[pulumi.Input[bool]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 wait_for_acceptance: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering PortfolioShare resources.
        :param pulumi.Input[str] accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
        :param pulumi.Input[bool] accepted: Whether the shared portfolio is imported by the recipient account. If the recipient is organizational, the share is automatically imported, and the field is always set to true.
        :param pulumi.Input[str] portfolio_id: Portfolio identifier.
        :param pulumi.Input[str] principal_id: Identifier of the principal with whom you will share the portfolio. Valid values AWS account IDs and ARNs of AWS Organizations and organizational units.
        :param pulumi.Input[bool] share_tag_options: Whether to enable sharing of `servicecatalog.TagOption` resources when creating the portfolio share.
        :param pulumi.Input[str] type: Type of portfolio share. Valid values are `ACCOUNT` (an external account), `ORGANIZATION` (a share to every account in an organization), `ORGANIZATIONAL_UNIT`, `ORGANIZATION_MEMBER_ACCOUNT` (a share to an account in an organization).
        :param pulumi.Input[bool] wait_for_acceptance: Whether to wait (up to the timeout) for the share to be accepted. Organizational shares are automatically accepted.
        """
        if accept_language is not None:
            pulumi.set(__self__, "accept_language", accept_language)
        if accepted is not None:
            pulumi.set(__self__, "accepted", accepted)
        if portfolio_id is not None:
            pulumi.set(__self__, "portfolio_id", portfolio_id)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if share_tag_options is not None:
            pulumi.set(__self__, "share_tag_options", share_tag_options)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if wait_for_acceptance is not None:
            pulumi.set(__self__, "wait_for_acceptance", wait_for_acceptance)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[pulumi.Input[str]]:
        """
        Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
        """
        return pulumi.get(self, "accept_language")

    @accept_language.setter
    def accept_language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accept_language", value)

    @property
    @pulumi.getter
    def accepted(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the shared portfolio is imported by the recipient account. If the recipient is organizational, the share is automatically imported, and the field is always set to true.
        """
        return pulumi.get(self, "accepted")

    @accepted.setter
    def accepted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "accepted", value)

    @property
    @pulumi.getter(name="portfolioId")
    def portfolio_id(self) -> Optional[pulumi.Input[str]]:
        """
        Portfolio identifier.
        """
        return pulumi.get(self, "portfolio_id")

    @portfolio_id.setter
    def portfolio_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "portfolio_id", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the principal with whom you will share the portfolio. Valid values AWS account IDs and ARNs of AWS Organizations and organizational units.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="shareTagOptions")
    def share_tag_options(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable sharing of `servicecatalog.TagOption` resources when creating the portfolio share.
        """
        return pulumi.get(self, "share_tag_options")

    @share_tag_options.setter
    def share_tag_options(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "share_tag_options", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of portfolio share. Valid values are `ACCOUNT` (an external account), `ORGANIZATION` (a share to every account in an organization), `ORGANIZATIONAL_UNIT`, `ORGANIZATION_MEMBER_ACCOUNT` (a share to an account in an organization).
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="waitForAcceptance")
    def wait_for_acceptance(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to wait (up to the timeout) for the share to be accepted. Organizational shares are automatically accepted.
        """
        return pulumi.get(self, "wait_for_acceptance")

    @wait_for_acceptance.setter
    def wait_for_acceptance(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_for_acceptance", value)


class PortfolioShare(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accept_language: Optional[pulumi.Input[str]] = None,
                 portfolio_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 share_tag_options: Optional[pulumi.Input[bool]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 wait_for_acceptance: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Manages a Service Catalog Portfolio Share. Shares the specified portfolio with the specified account or organization node. You can share portfolios to an organization, an organizational unit, or a specific account.

        If the portfolio share with the specified account or organization node already exists, using this resource to re-create the share will have no effect and will not return an error. You can then use this resource to update the share.

        > **NOTE:** Shares to an organization node can only be created by the management account of an organization or by a delegated administrator. If a delegated admin is de-registered, they can no longer create portfolio shares.

        > **NOTE:** AWSOrganizationsAccess must be enabled in order to create a portfolio share to an organization node.

        > **NOTE:** You can't share a shared resource, including portfolios that contain a shared product.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.servicecatalog.PortfolioShare("example",
            principal_id="012128675309",
            portfolio_id=aws_servicecatalog_portfolio["example"]["id"],
            type="ACCOUNT")
        ```

        ## Import

        `aws_servicecatalog_portfolio_share` can be imported using the portfolio share ID, e.g.

        ```sh
         $ pulumi import aws:servicecatalog/portfolioShare:PortfolioShare example port-12344321:ACCOUNT:123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
        :param pulumi.Input[str] portfolio_id: Portfolio identifier.
        :param pulumi.Input[str] principal_id: Identifier of the principal with whom you will share the portfolio. Valid values AWS account IDs and ARNs of AWS Organizations and organizational units.
        :param pulumi.Input[bool] share_tag_options: Whether to enable sharing of `servicecatalog.TagOption` resources when creating the portfolio share.
        :param pulumi.Input[str] type: Type of portfolio share. Valid values are `ACCOUNT` (an external account), `ORGANIZATION` (a share to every account in an organization), `ORGANIZATIONAL_UNIT`, `ORGANIZATION_MEMBER_ACCOUNT` (a share to an account in an organization).
        :param pulumi.Input[bool] wait_for_acceptance: Whether to wait (up to the timeout) for the share to be accepted. Organizational shares are automatically accepted.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PortfolioShareArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Service Catalog Portfolio Share. Shares the specified portfolio with the specified account or organization node. You can share portfolios to an organization, an organizational unit, or a specific account.

        If the portfolio share with the specified account or organization node already exists, using this resource to re-create the share will have no effect and will not return an error. You can then use this resource to update the share.

        > **NOTE:** Shares to an organization node can only be created by the management account of an organization or by a delegated administrator. If a delegated admin is de-registered, they can no longer create portfolio shares.

        > **NOTE:** AWSOrganizationsAccess must be enabled in order to create a portfolio share to an organization node.

        > **NOTE:** You can't share a shared resource, including portfolios that contain a shared product.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.servicecatalog.PortfolioShare("example",
            principal_id="012128675309",
            portfolio_id=aws_servicecatalog_portfolio["example"]["id"],
            type="ACCOUNT")
        ```

        ## Import

        `aws_servicecatalog_portfolio_share` can be imported using the portfolio share ID, e.g.

        ```sh
         $ pulumi import aws:servicecatalog/portfolioShare:PortfolioShare example port-12344321:ACCOUNT:123456789012
        ```

        :param str resource_name: The name of the resource.
        :param PortfolioShareArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PortfolioShareArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accept_language: Optional[pulumi.Input[str]] = None,
                 portfolio_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 share_tag_options: Optional[pulumi.Input[bool]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 wait_for_acceptance: Optional[pulumi.Input[bool]] = None,
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
            __props__ = PortfolioShareArgs.__new__(PortfolioShareArgs)

            __props__.__dict__["accept_language"] = accept_language
            if portfolio_id is None and not opts.urn:
                raise TypeError("Missing required property 'portfolio_id'")
            __props__.__dict__["portfolio_id"] = portfolio_id
            if principal_id is None and not opts.urn:
                raise TypeError("Missing required property 'principal_id'")
            __props__.__dict__["principal_id"] = principal_id
            __props__.__dict__["share_tag_options"] = share_tag_options
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["wait_for_acceptance"] = wait_for_acceptance
            __props__.__dict__["accepted"] = None
        super(PortfolioShare, __self__).__init__(
            'aws:servicecatalog/portfolioShare:PortfolioShare',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accept_language: Optional[pulumi.Input[str]] = None,
            accepted: Optional[pulumi.Input[bool]] = None,
            portfolio_id: Optional[pulumi.Input[str]] = None,
            principal_id: Optional[pulumi.Input[str]] = None,
            share_tag_options: Optional[pulumi.Input[bool]] = None,
            type: Optional[pulumi.Input[str]] = None,
            wait_for_acceptance: Optional[pulumi.Input[bool]] = None) -> 'PortfolioShare':
        """
        Get an existing PortfolioShare resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
        :param pulumi.Input[bool] accepted: Whether the shared portfolio is imported by the recipient account. If the recipient is organizational, the share is automatically imported, and the field is always set to true.
        :param pulumi.Input[str] portfolio_id: Portfolio identifier.
        :param pulumi.Input[str] principal_id: Identifier of the principal with whom you will share the portfolio. Valid values AWS account IDs and ARNs of AWS Organizations and organizational units.
        :param pulumi.Input[bool] share_tag_options: Whether to enable sharing of `servicecatalog.TagOption` resources when creating the portfolio share.
        :param pulumi.Input[str] type: Type of portfolio share. Valid values are `ACCOUNT` (an external account), `ORGANIZATION` (a share to every account in an organization), `ORGANIZATIONAL_UNIT`, `ORGANIZATION_MEMBER_ACCOUNT` (a share to an account in an organization).
        :param pulumi.Input[bool] wait_for_acceptance: Whether to wait (up to the timeout) for the share to be accepted. Organizational shares are automatically accepted.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PortfolioShareState.__new__(_PortfolioShareState)

        __props__.__dict__["accept_language"] = accept_language
        __props__.__dict__["accepted"] = accepted
        __props__.__dict__["portfolio_id"] = portfolio_id
        __props__.__dict__["principal_id"] = principal_id
        __props__.__dict__["share_tag_options"] = share_tag_options
        __props__.__dict__["type"] = type
        __props__.__dict__["wait_for_acceptance"] = wait_for_acceptance
        return PortfolioShare(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> pulumi.Output[Optional[str]]:
        """
        Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
        """
        return pulumi.get(self, "accept_language")

    @property
    @pulumi.getter
    def accepted(self) -> pulumi.Output[bool]:
        """
        Whether the shared portfolio is imported by the recipient account. If the recipient is organizational, the share is automatically imported, and the field is always set to true.
        """
        return pulumi.get(self, "accepted")

    @property
    @pulumi.getter(name="portfolioId")
    def portfolio_id(self) -> pulumi.Output[str]:
        """
        Portfolio identifier.
        """
        return pulumi.get(self, "portfolio_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Output[str]:
        """
        Identifier of the principal with whom you will share the portfolio. Valid values AWS account IDs and ARNs of AWS Organizations and organizational units.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="shareTagOptions")
    def share_tag_options(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to enable sharing of `servicecatalog.TagOption` resources when creating the portfolio share.
        """
        return pulumi.get(self, "share_tag_options")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of portfolio share. Valid values are `ACCOUNT` (an external account), `ORGANIZATION` (a share to every account in an organization), `ORGANIZATIONAL_UNIT`, `ORGANIZATION_MEMBER_ACCOUNT` (a share to an account in an organization).
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="waitForAcceptance")
    def wait_for_acceptance(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to wait (up to the timeout) for the share to be accepted. Organizational shares are automatically accepted.
        """
        return pulumi.get(self, "wait_for_acceptance")

