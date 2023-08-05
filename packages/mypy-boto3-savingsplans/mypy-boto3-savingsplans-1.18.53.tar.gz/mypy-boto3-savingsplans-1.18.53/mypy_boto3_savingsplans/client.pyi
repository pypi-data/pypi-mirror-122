"""
Type annotations for savingsplans service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_savingsplans import SavingsPlansClient

    client: SavingsPlansClient = boto3.client("savingsplans")
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from botocore.client import BaseClient, ClientMeta

from .literals import (
    CurrencyCodeType,
    SavingsPlanPaymentOptionType,
    SavingsPlanProductTypeType,
    SavingsPlanRateServiceCodeType,
    SavingsPlanStateType,
    SavingsPlanTypeType,
)
from .type_defs import (
    CreateSavingsPlanResponseTypeDef,
    DescribeSavingsPlanRatesResponseTypeDef,
    DescribeSavingsPlansOfferingRatesResponseTypeDef,
    DescribeSavingsPlansOfferingsResponseTypeDef,
    DescribeSavingsPlansResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    SavingsPlanFilterTypeDef,
    SavingsPlanOfferingFilterElementTypeDef,
    SavingsPlanOfferingRateFilterElementTypeDef,
    SavingsPlanRateFilterTypeDef,
)

__all__ = ("SavingsPlansClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SavingsPlansClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html)
    """

    meta: ClientMeta
    @property
    def exceptions(self) -> Exceptions:
        """
        SavingsPlansClient exceptions.
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#can_paginate)
        """
    def create_savings_plan(
        self,
        *,
        savingsPlanOfferingId: str,
        commitment: str,
        upfrontPaymentAmount: str = ...,
        purchaseTime: Union[datetime, str] = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateSavingsPlanResponseTypeDef:
        """
        Creates a Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.create_savings_plan)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#create_savings_plan)
        """
    def delete_queued_savings_plan(self, *, savingsPlanId: str) -> Dict[str, Any]:
        """
        Deletes the queued purchase for the specified Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.delete_queued_savings_plan)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#delete_queued_savings_plan)
        """
    def describe_savings_plan_rates(
        self,
        *,
        savingsPlanId: str,
        filters: Sequence["SavingsPlanRateFilterTypeDef"] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeSavingsPlanRatesResponseTypeDef:
        """
        Describes the specified Savings Plans rates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.describe_savings_plan_rates)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#describe_savings_plan_rates)
        """
    def describe_savings_plans(
        self,
        *,
        savingsPlanArns: Sequence[str] = ...,
        savingsPlanIds: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        states: Sequence[SavingsPlanStateType] = ...,
        filters: Sequence["SavingsPlanFilterTypeDef"] = ...
    ) -> DescribeSavingsPlansResponseTypeDef:
        """
        Describes the specified Savings Plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.describe_savings_plans)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#describe_savings_plans)
        """
    def describe_savings_plans_offering_rates(
        self,
        *,
        savingsPlanOfferingIds: Sequence[str] = ...,
        savingsPlanPaymentOptions: Sequence[SavingsPlanPaymentOptionType] = ...,
        savingsPlanTypes: Sequence[SavingsPlanTypeType] = ...,
        products: Sequence[SavingsPlanProductTypeType] = ...,
        serviceCodes: Sequence[SavingsPlanRateServiceCodeType] = ...,
        usageTypes: Sequence[str] = ...,
        operations: Sequence[str] = ...,
        filters: Sequence["SavingsPlanOfferingRateFilterElementTypeDef"] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeSavingsPlansOfferingRatesResponseTypeDef:
        """
        Describes the specified Savings Plans offering rates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.describe_savings_plans_offering_rates)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#describe_savings_plans_offering_rates)
        """
    def describe_savings_plans_offerings(
        self,
        *,
        offeringIds: Sequence[str] = ...,
        paymentOptions: Sequence[SavingsPlanPaymentOptionType] = ...,
        productType: SavingsPlanProductTypeType = ...,
        planTypes: Sequence[SavingsPlanTypeType] = ...,
        durations: Sequence[int] = ...,
        currencies: Sequence[CurrencyCodeType] = ...,
        descriptions: Sequence[str] = ...,
        serviceCodes: Sequence[str] = ...,
        usageTypes: Sequence[str] = ...,
        operations: Sequence[str] = ...,
        filters: Sequence["SavingsPlanOfferingFilterElementTypeDef"] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeSavingsPlansOfferingsResponseTypeDef:
        """
        Describes the specified Savings Plans offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.describe_savings_plans_offerings)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#describe_savings_plans_offerings)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#generate_presigned_url)
        """
    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#list_tags_for_resource)
        """
    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#tag_resource)
        """
    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/savingsplans.html#SavingsPlans.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_savingsplans/client.html#untag_resource)
        """
