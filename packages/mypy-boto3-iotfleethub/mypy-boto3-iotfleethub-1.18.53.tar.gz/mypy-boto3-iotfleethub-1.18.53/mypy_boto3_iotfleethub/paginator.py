"""
Type annotations for iotfleethub service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotfleethub/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_iotfleethub import IoTFleetHubClient
    from mypy_boto3_iotfleethub.paginator import (
        ListApplicationsPaginator,
    )

    client: IoTFleetHubClient = boto3.client("iotfleethub")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import ListApplicationsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListApplicationsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotfleethub.html#IoTFleetHub.Paginator.ListApplications)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotfleethub/paginators.html#listapplicationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/iotfleethub.html#IoTFleetHub.Paginator.ListApplications.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iotfleethub/paginators.html#listapplicationspaginator)
        """
