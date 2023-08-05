"""
Type annotations for iotsitewise service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_iotsitewise import IoTSiteWiseClient
    from mypy_boto3_iotsitewise.paginator import (
        GetAssetPropertyAggregatesPaginator,
        GetAssetPropertyValueHistoryPaginator,
        GetInterpolatedAssetPropertyValuesPaginator,
        ListAccessPoliciesPaginator,
        ListAssetModelsPaginator,
        ListAssetRelationshipsPaginator,
        ListAssetsPaginator,
        ListAssociatedAssetsPaginator,
        ListDashboardsPaginator,
        ListGatewaysPaginator,
        ListPortalsPaginator,
        ListProjectAssetsPaginator,
        ListProjectsPaginator,
    )

    client: IoTSiteWiseClient = boto3.client("iotsitewise")

    get_asset_property_aggregates_paginator: GetAssetPropertyAggregatesPaginator = client.get_paginator("get_asset_property_aggregates")
    get_asset_property_value_history_paginator: GetAssetPropertyValueHistoryPaginator = client.get_paginator("get_asset_property_value_history")
    get_interpolated_asset_property_values_paginator: GetInterpolatedAssetPropertyValuesPaginator = client.get_paginator("get_interpolated_asset_property_values")
    list_access_policies_paginator: ListAccessPoliciesPaginator = client.get_paginator("list_access_policies")
    list_asset_models_paginator: ListAssetModelsPaginator = client.get_paginator("list_asset_models")
    list_asset_relationships_paginator: ListAssetRelationshipsPaginator = client.get_paginator("list_asset_relationships")
    list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
    list_associated_assets_paginator: ListAssociatedAssetsPaginator = client.get_paginator("list_associated_assets")
    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_portals_paginator: ListPortalsPaginator = client.get_paginator("list_portals")
    list_project_assets_paginator: ListProjectAssetsPaginator = client.get_paginator("list_project_assets")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    AggregateTypeType,
    IdentityTypeType,
    ListAssetsFilterType,
    QualityType,
    ResourceTypeType,
    TimeOrderingType,
    TraversalDirectionType,
)
from .type_defs import (
    GetAssetPropertyAggregatesResponseTypeDef,
    GetAssetPropertyValueHistoryResponseTypeDef,
    GetInterpolatedAssetPropertyValuesResponseTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListAssetModelsResponseTypeDef,
    ListAssetRelationshipsResponseTypeDef,
    ListAssetsResponseTypeDef,
    ListAssociatedAssetsResponseTypeDef,
    ListDashboardsResponseTypeDef,
    ListGatewaysResponseTypeDef,
    ListPortalsResponseTypeDef,
    ListProjectAssetsResponseTypeDef,
    ListProjectsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "GetAssetPropertyAggregatesPaginator",
    "GetAssetPropertyValueHistoryPaginator",
    "GetInterpolatedAssetPropertyValuesPaginator",
    "ListAccessPoliciesPaginator",
    "ListAssetModelsPaginator",
    "ListAssetRelationshipsPaginator",
    "ListAssetsPaginator",
    "ListAssociatedAssetsPaginator",
    "ListDashboardsPaginator",
    "ListGatewaysPaginator",
    "ListPortalsPaginator",
    "ListProjectAssetsPaginator",
    "ListProjectsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetAssetPropertyAggregatesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.GetAssetPropertyAggregates)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#getassetpropertyaggregatespaginator)
    """

    def paginate(
        self,
        *,
        aggregateTypes: Sequence[AggregateTypeType],
        resolution: str,
        startDate: Union[datetime, str],
        endDate: Union[datetime, str],
        assetId: str = ...,
        propertyId: str = ...,
        propertyAlias: str = ...,
        qualities: Sequence[QualityType] = ...,
        timeOrdering: TimeOrderingType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAssetPropertyAggregatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.GetAssetPropertyAggregates.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#getassetpropertyaggregatespaginator)
        """

class GetAssetPropertyValueHistoryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.GetAssetPropertyValueHistory)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#getassetpropertyvaluehistorypaginator)
    """

    def paginate(
        self,
        *,
        assetId: str = ...,
        propertyId: str = ...,
        propertyAlias: str = ...,
        startDate: Union[datetime, str] = ...,
        endDate: Union[datetime, str] = ...,
        qualities: Sequence[QualityType] = ...,
        timeOrdering: TimeOrderingType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetAssetPropertyValueHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.GetAssetPropertyValueHistory.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#getassetpropertyvaluehistorypaginator)
        """

class GetInterpolatedAssetPropertyValuesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.GetInterpolatedAssetPropertyValues)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#getinterpolatedassetpropertyvaluespaginator)
    """

    def paginate(
        self,
        *,
        startTimeInSeconds: int,
        endTimeInSeconds: int,
        quality: QualityType,
        intervalInSeconds: int,
        type: str,
        assetId: str = ...,
        propertyId: str = ...,
        propertyAlias: str = ...,
        startTimeOffsetInNanos: int = ...,
        endTimeOffsetInNanos: int = ...,
        intervalWindowInSeconds: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetInterpolatedAssetPropertyValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.GetInterpolatedAssetPropertyValues.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#getinterpolatedassetpropertyvaluespaginator)
        """

class ListAccessPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAccessPolicies)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listaccesspoliciespaginator)
    """

    def paginate(
        self,
        *,
        identityType: IdentityTypeType = ...,
        identityId: str = ...,
        resourceType: ResourceTypeType = ...,
        resourceId: str = ...,
        iamArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccessPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAccessPolicies.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listaccesspoliciespaginator)
        """

class ListAssetModelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssetModels)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassetmodelspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssetModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssetModels.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassetmodelspaginator)
        """

class ListAssetRelationshipsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssetRelationships)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassetrelationshipspaginator)
    """

    def paginate(
        self,
        *,
        assetId: str,
        traversalType: Literal["PATH_TO_ROOT"],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssetRelationshipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssetRelationships.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassetrelationshipspaginator)
        """

class ListAssetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassetspaginator)
    """

    def paginate(
        self,
        *,
        assetModelId: str = ...,
        filter: ListAssetsFilterType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassetspaginator)
        """

class ListAssociatedAssetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssociatedAssets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassociatedassetspaginator)
    """

    def paginate(
        self,
        *,
        assetId: str,
        hierarchyId: str = ...,
        traversalDirection: TraversalDirectionType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociatedAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListAssociatedAssets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listassociatedassetspaginator)
        """

class ListDashboardsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListDashboards)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listdashboardspaginator)
    """

    def paginate(
        self, *, projectId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListDashboards.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listdashboardspaginator)
        """

class ListGatewaysPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListGateways)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listgatewayspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListGateways.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listgatewayspaginator)
        """

class ListPortalsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListPortals)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listportalspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPortalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListPortals.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listportalspaginator)
        """

class ListProjectAssetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListProjectAssets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listprojectassetspaginator)
    """

    def paginate(
        self, *, projectId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProjectAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListProjectAssets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listprojectassetspaginator)
        """

class ListProjectsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListProjects)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listprojectspaginator)
    """

    def paginate(
        self, *, portalId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotsitewise.html#IoTSiteWise.Paginator.ListProjects.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/paginators.html#listprojectspaginator)
        """
