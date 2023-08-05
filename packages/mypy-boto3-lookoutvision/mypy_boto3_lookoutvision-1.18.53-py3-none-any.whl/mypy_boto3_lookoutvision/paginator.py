"""
Type annotations for lookoutvision service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_lookoutvision import LookoutforVisionClient
    from mypy_boto3_lookoutvision.paginator import (
        ListDatasetEntriesPaginator,
        ListModelsPaginator,
        ListProjectsPaginator,
    )

    client: LookoutforVisionClient = boto3.client("lookoutvision")

    list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
    list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListDatasetEntriesResponseTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListDatasetEntriesPaginator", "ListModelsPaginator", "ListProjectsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDatasetEntriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListDatasetEntries)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators.html#listdatasetentriespaginator)
    """

    def paginate(
        self,
        *,
        ProjectName: str,
        DatasetType: str,
        Labeled: bool = ...,
        AnomalyClass: str = ...,
        BeforeCreationDate: Union[datetime, str] = ...,
        AfterCreationDate: Union[datetime, str] = ...,
        SourceRefContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListDatasetEntries.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators.html#listdatasetentriespaginator)
        """


class ListModelsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModels)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators.html#listmodelspaginator)
    """

    def paginate(
        self, *, ProjectName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListModels.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators.html#listmodelspaginator)
        """


class ListProjectsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListProjects)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators.html#listprojectspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/lookoutvision.html#LookoutforVision.Paginator.ListProjects.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lookoutvision/paginators.html#listprojectspaginator)
        """
