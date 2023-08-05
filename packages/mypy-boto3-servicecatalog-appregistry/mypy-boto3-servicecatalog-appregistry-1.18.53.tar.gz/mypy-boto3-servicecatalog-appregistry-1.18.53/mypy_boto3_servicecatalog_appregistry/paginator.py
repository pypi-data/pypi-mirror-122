"""
Type annotations for servicecatalog-appregistry service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_servicecatalog_appregistry import AppRegistryClient
    from mypy_boto3_servicecatalog_appregistry.paginator import (
        ListApplicationsPaginator,
        ListAssociatedAttributeGroupsPaginator,
        ListAssociatedResourcesPaginator,
        ListAttributeGroupsPaginator,
    )

    client: AppRegistryClient = boto3.client("servicecatalog-appregistry")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_associated_attribute_groups_paginator: ListAssociatedAttributeGroupsPaginator = client.get_paginator("list_associated_attribute_groups")
    list_associated_resources_paginator: ListAssociatedResourcesPaginator = client.get_paginator("list_associated_resources")
    list_attribute_groups_paginator: ListAttributeGroupsPaginator = client.get_paginator("list_attribute_groups")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListApplicationsResponseTypeDef,
    ListAssociatedAttributeGroupsResponseTypeDef,
    ListAssociatedResourcesResponseTypeDef,
    ListAttributeGroupsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListApplicationsPaginator",
    "ListAssociatedAttributeGroupsPaginator",
    "ListAssociatedResourcesPaginator",
    "ListAttributeGroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListApplications)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listapplicationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListApplications.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listapplicationspaginator)
        """


class ListAssociatedAttributeGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedAttributeGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listassociatedattributegroupspaginator)
    """

    def paginate(
        self, *, application: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociatedAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedAttributeGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listassociatedattributegroupspaginator)
        """


class ListAssociatedResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedResources)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listassociatedresourcespaginator)
    """

    def paginate(
        self, *, application: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAssociatedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAssociatedResources.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listassociatedresourcespaginator)
        """


class ListAttributeGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAttributeGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listattributegroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttributeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/servicecatalog-appregistry.html#AppRegistry.Paginator.ListAttributeGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/paginators.html#listattributegroupspaginator)
        """
