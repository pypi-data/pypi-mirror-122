# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['TriggerArgs', 'Trigger']

@pulumi.input_type
class TriggerArgs:
    def __init__(__self__, *,
                 actions: pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]],
                 type: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 predicate: Optional[pulumi.Input['TriggerPredicateArgs']] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workflow_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Trigger resource.
        :param pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]] actions: List of actions initiated by this trigger when it fires. See Actions Below.
        :param pulumi.Input[str] type: The type of trigger. Valid values are `CONDITIONAL`, `ON_DEMAND`, and `SCHEDULED`.
        :param pulumi.Input[str] description: A description of the new trigger.
        :param pulumi.Input[bool] enabled: Start the trigger. Defaults to `true`.
        :param pulumi.Input[str] name: The name of the trigger.
        :param pulumi.Input['TriggerPredicateArgs'] predicate: A predicate to specify when the new trigger should fire. Required when trigger type is `CONDITIONAL`. See Predicate Below.
        :param pulumi.Input[str] schedule: A cron expression used to specify the schedule. [Time-Based Schedules for Jobs and Crawlers](https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] workflow_name: A workflow to which the trigger should be associated to. Every workflow graph (DAG) needs a starting trigger (`ON_DEMAND` or `SCHEDULED` type) and can contain multiple additional `CONDITIONAL` triggers.
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "type", type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if predicate is not None:
            pulumi.set(__self__, "predicate", predicate)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if workflow_name is not None:
            pulumi.set(__self__, "workflow_name", workflow_name)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]]:
        """
        List of actions initiated by this trigger when it fires. See Actions Below.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of trigger. Valid values are `CONDITIONAL`, `ON_DEMAND`, and `SCHEDULED`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the new trigger.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Start the trigger. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the trigger.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def predicate(self) -> Optional[pulumi.Input['TriggerPredicateArgs']]:
        """
        A predicate to specify when the new trigger should fire. Required when trigger type is `CONDITIONAL`. See Predicate Below.
        """
        return pulumi.get(self, "predicate")

    @predicate.setter
    def predicate(self, value: Optional[pulumi.Input['TriggerPredicateArgs']]):
        pulumi.set(self, "predicate", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input[str]]:
        """
        A cron expression used to specify the schedule. [Time-Based Schedules for Jobs and Crawlers](https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html)
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="workflowName")
    def workflow_name(self) -> Optional[pulumi.Input[str]]:
        """
        A workflow to which the trigger should be associated to. Every workflow graph (DAG) needs a starting trigger (`ON_DEMAND` or `SCHEDULED` type) and can contain multiple additional `CONDITIONAL` triggers.
        """
        return pulumi.get(self, "workflow_name")

    @workflow_name.setter
    def workflow_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workflow_name", value)


@pulumi.input_type
class _TriggerState:
    def __init__(__self__, *,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 predicate: Optional[pulumi.Input['TriggerPredicateArgs']] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Trigger resources.
        :param pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]] actions: List of actions initiated by this trigger when it fires. See Actions Below.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of Glue Trigger
        :param pulumi.Input[str] description: A description of the new trigger.
        :param pulumi.Input[bool] enabled: Start the trigger. Defaults to `true`.
        :param pulumi.Input[str] name: The name of the trigger.
        :param pulumi.Input['TriggerPredicateArgs'] predicate: A predicate to specify when the new trigger should fire. Required when trigger type is `CONDITIONAL`. See Predicate Below.
        :param pulumi.Input[str] schedule: A cron expression used to specify the schedule. [Time-Based Schedules for Jobs and Crawlers](https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html)
        :param pulumi.Input[str] state: The condition job state. Currently, the values supported are `SUCCEEDED`, `STOPPED`, `TIMEOUT` and `FAILED`. If this is specified, `job_name` must also be specified. Conflicts with `crawler_state`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: The type of trigger. Valid values are `CONDITIONAL`, `ON_DEMAND`, and `SCHEDULED`.
        :param pulumi.Input[str] workflow_name: A workflow to which the trigger should be associated to. Every workflow graph (DAG) needs a starting trigger (`ON_DEMAND` or `SCHEDULED` type) and can contain multiple additional `CONDITIONAL` triggers.
        """
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if predicate is not None:
            pulumi.set(__self__, "predicate", predicate)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if workflow_name is not None:
            pulumi.set(__self__, "workflow_name", workflow_name)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]]]:
        """
        List of actions initiated by this trigger when it fires. See Actions Below.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TriggerActionArgs']]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of Glue Trigger
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the new trigger.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Start the trigger. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the trigger.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def predicate(self) -> Optional[pulumi.Input['TriggerPredicateArgs']]:
        """
        A predicate to specify when the new trigger should fire. Required when trigger type is `CONDITIONAL`. See Predicate Below.
        """
        return pulumi.get(self, "predicate")

    @predicate.setter
    def predicate(self, value: Optional[pulumi.Input['TriggerPredicateArgs']]):
        pulumi.set(self, "predicate", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input[str]]:
        """
        A cron expression used to specify the schedule. [Time-Based Schedules for Jobs and Crawlers](https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html)
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The condition job state. Currently, the values supported are `SUCCEEDED`, `STOPPED`, `TIMEOUT` and `FAILED`. If this is specified, `job_name` must also be specified. Conflicts with `crawler_state`.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of trigger. Valid values are `CONDITIONAL`, `ON_DEMAND`, and `SCHEDULED`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="workflowName")
    def workflow_name(self) -> Optional[pulumi.Input[str]]:
        """
        A workflow to which the trigger should be associated to. Every workflow graph (DAG) needs a starting trigger (`ON_DEMAND` or `SCHEDULED` type) and can contain multiple additional `CONDITIONAL` triggers.
        """
        return pulumi.get(self, "workflow_name")

    @workflow_name.setter
    def workflow_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workflow_name", value)


class Trigger(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TriggerActionArgs']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 predicate: Optional[pulumi.Input[pulumi.InputType['TriggerPredicateArgs']]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Glue Trigger resource.

        ## Example Usage
        ### Conditional Trigger

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="CONDITIONAL",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example1"]["name"],
            )],
            predicate=aws.glue.TriggerPredicateArgs(
                conditions=[aws.glue.TriggerPredicateConditionArgs(
                    job_name=aws_glue_job["example2"]["name"],
                    state="SUCCEEDED",
                )],
            ))
        ```
        ### On-Demand Trigger

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="ON_DEMAND",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example"]["name"],
            )])
        ```
        ### Scheduled Trigger

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            schedule="cron(15 12 * * ? *)",
            type="SCHEDULED",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example"]["name"],
            )])
        ```
        ### Conditional Trigger with Crawler Action

        **Note:** Triggers can have both a crawler action and a crawler condition, just no example provided.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="CONDITIONAL",
            actions=[aws.glue.TriggerActionArgs(
                crawler_name=aws_glue_crawler["example1"]["name"],
            )],
            predicate=aws.glue.TriggerPredicateArgs(
                conditions=[aws.glue.TriggerPredicateConditionArgs(
                    job_name=aws_glue_job["example2"]["name"],
                    state="SUCCEEDED",
                )],
            ))
        ```
        ### Conditional Trigger with Crawler Condition

        **Note:** Triggers can have both a crawler action and a crawler condition, just no example provided.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="CONDITIONAL",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example1"]["name"],
            )],
            predicate=aws.glue.TriggerPredicateArgs(
                conditions=[aws.glue.TriggerPredicateConditionArgs(
                    crawler_name=aws_glue_crawler["example2"]["name"],
                    crawl_state="SUCCEEDED",
                )],
            ))
        ```

        ## Import

        Glue Triggers can be imported using `name`, e.g.

        ```sh
         $ pulumi import aws:glue/trigger:Trigger MyTrigger MyTrigger
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TriggerActionArgs']]]] actions: List of actions initiated by this trigger when it fires. See Actions Below.
        :param pulumi.Input[str] description: A description of the new trigger.
        :param pulumi.Input[bool] enabled: Start the trigger. Defaults to `true`.
        :param pulumi.Input[str] name: The name of the trigger.
        :param pulumi.Input[pulumi.InputType['TriggerPredicateArgs']] predicate: A predicate to specify when the new trigger should fire. Required when trigger type is `CONDITIONAL`. See Predicate Below.
        :param pulumi.Input[str] schedule: A cron expression used to specify the schedule. [Time-Based Schedules for Jobs and Crawlers](https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: The type of trigger. Valid values are `CONDITIONAL`, `ON_DEMAND`, and `SCHEDULED`.
        :param pulumi.Input[str] workflow_name: A workflow to which the trigger should be associated to. Every workflow graph (DAG) needs a starting trigger (`ON_DEMAND` or `SCHEDULED` type) and can contain multiple additional `CONDITIONAL` triggers.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TriggerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Glue Trigger resource.

        ## Example Usage
        ### Conditional Trigger

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="CONDITIONAL",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example1"]["name"],
            )],
            predicate=aws.glue.TriggerPredicateArgs(
                conditions=[aws.glue.TriggerPredicateConditionArgs(
                    job_name=aws_glue_job["example2"]["name"],
                    state="SUCCEEDED",
                )],
            ))
        ```
        ### On-Demand Trigger

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="ON_DEMAND",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example"]["name"],
            )])
        ```
        ### Scheduled Trigger

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            schedule="cron(15 12 * * ? *)",
            type="SCHEDULED",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example"]["name"],
            )])
        ```
        ### Conditional Trigger with Crawler Action

        **Note:** Triggers can have both a crawler action and a crawler condition, just no example provided.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="CONDITIONAL",
            actions=[aws.glue.TriggerActionArgs(
                crawler_name=aws_glue_crawler["example1"]["name"],
            )],
            predicate=aws.glue.TriggerPredicateArgs(
                conditions=[aws.glue.TriggerPredicateConditionArgs(
                    job_name=aws_glue_job["example2"]["name"],
                    state="SUCCEEDED",
                )],
            ))
        ```
        ### Conditional Trigger with Crawler Condition

        **Note:** Triggers can have both a crawler action and a crawler condition, just no example provided.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.Trigger("example",
            type="CONDITIONAL",
            actions=[aws.glue.TriggerActionArgs(
                job_name=aws_glue_job["example1"]["name"],
            )],
            predicate=aws.glue.TriggerPredicateArgs(
                conditions=[aws.glue.TriggerPredicateConditionArgs(
                    crawler_name=aws_glue_crawler["example2"]["name"],
                    crawl_state="SUCCEEDED",
                )],
            ))
        ```

        ## Import

        Glue Triggers can be imported using `name`, e.g.

        ```sh
         $ pulumi import aws:glue/trigger:Trigger MyTrigger MyTrigger
        ```

        :param str resource_name: The name of the resource.
        :param TriggerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TriggerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TriggerActionArgs']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 predicate: Optional[pulumi.Input[pulumi.InputType['TriggerPredicateArgs']]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 workflow_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = TriggerArgs.__new__(TriggerArgs)

            if actions is None and not opts.urn:
                raise TypeError("Missing required property 'actions'")
            __props__.__dict__["actions"] = actions
            __props__.__dict__["description"] = description
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["name"] = name
            __props__.__dict__["predicate"] = predicate
            __props__.__dict__["schedule"] = schedule
            __props__.__dict__["tags"] = tags
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["workflow_name"] = workflow_name
            __props__.__dict__["arn"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["tags_all"] = None
        super(Trigger, __self__).__init__(
            'aws:glue/trigger:Trigger',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            actions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TriggerActionArgs']]]]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            predicate: Optional[pulumi.Input[pulumi.InputType['TriggerPredicateArgs']]] = None,
            schedule: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            type: Optional[pulumi.Input[str]] = None,
            workflow_name: Optional[pulumi.Input[str]] = None) -> 'Trigger':
        """
        Get an existing Trigger resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TriggerActionArgs']]]] actions: List of actions initiated by this trigger when it fires. See Actions Below.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of Glue Trigger
        :param pulumi.Input[str] description: A description of the new trigger.
        :param pulumi.Input[bool] enabled: Start the trigger. Defaults to `true`.
        :param pulumi.Input[str] name: The name of the trigger.
        :param pulumi.Input[pulumi.InputType['TriggerPredicateArgs']] predicate: A predicate to specify when the new trigger should fire. Required when trigger type is `CONDITIONAL`. See Predicate Below.
        :param pulumi.Input[str] schedule: A cron expression used to specify the schedule. [Time-Based Schedules for Jobs and Crawlers](https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html)
        :param pulumi.Input[str] state: The condition job state. Currently, the values supported are `SUCCEEDED`, `STOPPED`, `TIMEOUT` and `FAILED`. If this is specified, `job_name` must also be specified. Conflicts with `crawler_state`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: The type of trigger. Valid values are `CONDITIONAL`, `ON_DEMAND`, and `SCHEDULED`.
        :param pulumi.Input[str] workflow_name: A workflow to which the trigger should be associated to. Every workflow graph (DAG) needs a starting trigger (`ON_DEMAND` or `SCHEDULED` type) and can contain multiple additional `CONDITIONAL` triggers.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TriggerState.__new__(_TriggerState)

        __props__.__dict__["actions"] = actions
        __props__.__dict__["arn"] = arn
        __props__.__dict__["description"] = description
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["name"] = name
        __props__.__dict__["predicate"] = predicate
        __props__.__dict__["schedule"] = schedule
        __props__.__dict__["state"] = state
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["type"] = type
        __props__.__dict__["workflow_name"] = workflow_name
        return Trigger(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output[Sequence['outputs.TriggerAction']]:
        """
        List of actions initiated by this trigger when it fires. See Actions Below.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of Glue Trigger
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the new trigger.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Start the trigger. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the trigger.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def predicate(self) -> pulumi.Output[Optional['outputs.TriggerPredicate']]:
        """
        A predicate to specify when the new trigger should fire. Required when trigger type is `CONDITIONAL`. See Predicate Below.
        """
        return pulumi.get(self, "predicate")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional[str]]:
        """
        A cron expression used to specify the schedule. [Time-Based Schedules for Jobs and Crawlers](https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html)
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The condition job state. Currently, the values supported are `SUCCEEDED`, `STOPPED`, `TIMEOUT` and `FAILED`. If this is specified, `job_name` must also be specified. Conflicts with `crawler_state`.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of trigger. Valid values are `CONDITIONAL`, `ON_DEMAND`, and `SCHEDULED`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workflowName")
    def workflow_name(self) -> pulumi.Output[Optional[str]]:
        """
        A workflow to which the trigger should be associated to. Every workflow graph (DAG) needs a starting trigger (`ON_DEMAND` or `SCHEDULED` type) and can contain multiple additional `CONDITIONAL` triggers.
        """
        return pulumi.get(self, "workflow_name")

