# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetAvailabilityZoneResult',
    'AwaitableGetAvailabilityZoneResult',
    'get_availability_zone',
    'get_availability_zone_output',
]

@pulumi.output_type
class GetAvailabilityZoneResult:
    """
    A collection of values returned by getAvailabilityZone.
    """
    def __init__(__self__, all_availability_zones=None, filters=None, group_name=None, id=None, name=None, name_suffix=None, network_border_group=None, opt_in_status=None, parent_zone_id=None, parent_zone_name=None, region=None, state=None, zone_id=None, zone_type=None):
        if all_availability_zones and not isinstance(all_availability_zones, bool):
            raise TypeError("Expected argument 'all_availability_zones' to be a bool")
        pulumi.set(__self__, "all_availability_zones", all_availability_zones)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if group_name and not isinstance(group_name, str):
            raise TypeError("Expected argument 'group_name' to be a str")
        pulumi.set(__self__, "group_name", group_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if name_suffix and not isinstance(name_suffix, str):
            raise TypeError("Expected argument 'name_suffix' to be a str")
        pulumi.set(__self__, "name_suffix", name_suffix)
        if network_border_group and not isinstance(network_border_group, str):
            raise TypeError("Expected argument 'network_border_group' to be a str")
        pulumi.set(__self__, "network_border_group", network_border_group)
        if opt_in_status and not isinstance(opt_in_status, str):
            raise TypeError("Expected argument 'opt_in_status' to be a str")
        pulumi.set(__self__, "opt_in_status", opt_in_status)
        if parent_zone_id and not isinstance(parent_zone_id, str):
            raise TypeError("Expected argument 'parent_zone_id' to be a str")
        pulumi.set(__self__, "parent_zone_id", parent_zone_id)
        if parent_zone_name and not isinstance(parent_zone_name, str):
            raise TypeError("Expected argument 'parent_zone_name' to be a str")
        pulumi.set(__self__, "parent_zone_name", parent_zone_name)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if zone_id and not isinstance(zone_id, str):
            raise TypeError("Expected argument 'zone_id' to be a str")
        pulumi.set(__self__, "zone_id", zone_id)
        if zone_type and not isinstance(zone_type, str):
            raise TypeError("Expected argument 'zone_type' to be a str")
        pulumi.set(__self__, "zone_type", zone_type)

    @property
    @pulumi.getter(name="allAvailabilityZones")
    def all_availability_zones(self) -> Optional[bool]:
        return pulumi.get(self, "all_availability_zones")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAvailabilityZoneFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> str:
        """
        For Availability Zones, this is the same value as the Region name. For Local Zones, the name of the associated group, for example `us-west-2-lax-1`.
        """
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nameSuffix")
    def name_suffix(self) -> str:
        """
        The part of the AZ name that appears after the region name, uniquely identifying the AZ within its region.
        For Availability Zones this is usually a single letter, for example `a` for the `us-west-2a` zone.
        For Local and Wavelength Zones this is a longer string, for example `wl1-sfo-wlz-1` for the `us-west-2-wl1-sfo-wlz-1` zone.
        """
        return pulumi.get(self, "name_suffix")

    @property
    @pulumi.getter(name="networkBorderGroup")
    def network_border_group(self) -> str:
        """
        The name of the location from which the address is advertised.
        """
        return pulumi.get(self, "network_border_group")

    @property
    @pulumi.getter(name="optInStatus")
    def opt_in_status(self) -> str:
        """
        For Availability Zones, this always has the value of `opt-in-not-required`. For Local Zones, this is the opt in status. The possible values are `opted-in` and `not-opted-in`.
        """
        return pulumi.get(self, "opt_in_status")

    @property
    @pulumi.getter(name="parentZoneId")
    def parent_zone_id(self) -> str:
        """
        The ID of the zone that handles some of the Local Zone or Wavelength Zone control plane operations, such as API calls.
        """
        return pulumi.get(self, "parent_zone_id")

    @property
    @pulumi.getter(name="parentZoneName")
    def parent_zone_name(self) -> str:
        """
        The name of the zone that handles some of the Local Zone or Wavelength Zone control plane operations, such as API calls.
        """
        return pulumi.get(self, "parent_zone_name")

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        The region where the selected availability zone resides. This is always the region selected on the provider, since this data source searches only within that region.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def state(self) -> str:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> str:
        return pulumi.get(self, "zone_id")

    @property
    @pulumi.getter(name="zoneType")
    def zone_type(self) -> str:
        """
        The type of zone. Values are `availability-zone`, `local-zone`, and `wavelength-zone`.
        """
        return pulumi.get(self, "zone_type")


class AwaitableGetAvailabilityZoneResult(GetAvailabilityZoneResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAvailabilityZoneResult(
            all_availability_zones=self.all_availability_zones,
            filters=self.filters,
            group_name=self.group_name,
            id=self.id,
            name=self.name,
            name_suffix=self.name_suffix,
            network_border_group=self.network_border_group,
            opt_in_status=self.opt_in_status,
            parent_zone_id=self.parent_zone_id,
            parent_zone_name=self.parent_zone_name,
            region=self.region,
            state=self.state,
            zone_id=self.zone_id,
            zone_type=self.zone_type)


def get_availability_zone(all_availability_zones: Optional[bool] = None,
                          filters: Optional[Sequence[pulumi.InputType['GetAvailabilityZoneFilterArgs']]] = None,
                          name: Optional[str] = None,
                          state: Optional[str] = None,
                          zone_id: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAvailabilityZoneResult:
    """
    `get_availability_zone` provides details about a specific availability zone (AZ)
    in the current region.

    This can be used both to validate an availability zone given in a variable
    and to split the AZ name into its component parts of an AWS region and an
    AZ identifier letter. The latter may be useful e.g. for implementing a
    consistent subnet numbering scheme across several regions by mapping both
    the region and the subnet letter to network numbers.

    This is different from the `get_availability_zones` (plural) data source,
    which provides a list of the available zones.


    :param bool all_availability_zones: Set to `true` to include all Availability Zones and Local Zones regardless of your opt in status.
    :param Sequence[pulumi.InputType['GetAvailabilityZoneFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    :param str name: The name of the filter field. Valid values can be found in the [EC2 DescribeAvailabilityZones API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAvailabilityZones.html).
    :param str state: A specific availability zone state to require. May be any of `"available"`, `"information"` or `"impaired"`.
    :param str zone_id: The zone ID of the availability zone to select.
    """
    __args__ = dict()
    __args__['allAvailabilityZones'] = all_availability_zones
    __args__['filters'] = filters
    __args__['name'] = name
    __args__['state'] = state
    __args__['zoneId'] = zone_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:index/getAvailabilityZone:getAvailabilityZone', __args__, opts=opts, typ=GetAvailabilityZoneResult).value

    return AwaitableGetAvailabilityZoneResult(
        all_availability_zones=__ret__.all_availability_zones,
        filters=__ret__.filters,
        group_name=__ret__.group_name,
        id=__ret__.id,
        name=__ret__.name,
        name_suffix=__ret__.name_suffix,
        network_border_group=__ret__.network_border_group,
        opt_in_status=__ret__.opt_in_status,
        parent_zone_id=__ret__.parent_zone_id,
        parent_zone_name=__ret__.parent_zone_name,
        region=__ret__.region,
        state=__ret__.state,
        zone_id=__ret__.zone_id,
        zone_type=__ret__.zone_type)


@_utilities.lift_output_func(get_availability_zone)
def get_availability_zone_output(all_availability_zones: Optional[pulumi.Input[Optional[bool]]] = None,
                                 filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAvailabilityZoneFilterArgs']]]]] = None,
                                 name: Optional[pulumi.Input[Optional[str]]] = None,
                                 state: Optional[pulumi.Input[Optional[str]]] = None,
                                 zone_id: Optional[pulumi.Input[Optional[str]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAvailabilityZoneResult]:
    """
    `get_availability_zone` provides details about a specific availability zone (AZ)
    in the current region.

    This can be used both to validate an availability zone given in a variable
    and to split the AZ name into its component parts of an AWS region and an
    AZ identifier letter. The latter may be useful e.g. for implementing a
    consistent subnet numbering scheme across several regions by mapping both
    the region and the subnet letter to network numbers.

    This is different from the `get_availability_zones` (plural) data source,
    which provides a list of the available zones.


    :param bool all_availability_zones: Set to `true` to include all Availability Zones and Local Zones regardless of your opt in status.
    :param Sequence[pulumi.InputType['GetAvailabilityZoneFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    :param str name: The name of the filter field. Valid values can be found in the [EC2 DescribeAvailabilityZones API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAvailabilityZones.html).
    :param str state: A specific availability zone state to require. May be any of `"available"`, `"information"` or `"impaired"`.
    :param str zone_id: The zone ID of the availability zone to select.
    """
    ...
