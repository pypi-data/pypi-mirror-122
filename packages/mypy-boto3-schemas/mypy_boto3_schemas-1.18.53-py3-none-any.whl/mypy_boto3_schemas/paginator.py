"""
Type annotations for schemas service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_schemas import SchemasClient
    from mypy_boto3_schemas.paginator import (
        ListDiscoverersPaginator,
        ListRegistriesPaginator,
        ListSchemaVersionsPaginator,
        ListSchemasPaginator,
        SearchSchemasPaginator,
    )

    client: SchemasClient = boto3.client("schemas")

    list_discoverers_paginator: ListDiscoverersPaginator = client.get_paginator("list_discoverers")
    list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
    list_schema_versions_paginator: ListSchemaVersionsPaginator = client.get_paginator("list_schema_versions")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    search_schemas_paginator: SearchSchemasPaginator = client.get_paginator("search_schemas")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListDiscoverersResponseTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsResponseTypeDef,
    PaginatorConfigTypeDef,
    SearchSchemasResponseTypeDef,
)

__all__ = (
    "ListDiscoverersPaginator",
    "ListRegistriesPaginator",
    "ListSchemaVersionsPaginator",
    "ListSchemasPaginator",
    "SearchSchemasPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDiscoverersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListDiscoverers)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listdiscovererspaginator)
    """

    def paginate(
        self,
        *,
        DiscovererIdPrefix: str = ...,
        SourceArnPrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDiscoverersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListDiscoverers.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listdiscovererspaginator)
        """


class ListRegistriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListRegistries)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listregistriespaginator)
    """

    def paginate(
        self,
        *,
        RegistryNamePrefix: str = ...,
        Scope: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListRegistries.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listregistriespaginator)
        """


class ListSchemaVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListSchemaVersions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listschemaversionspaginator)
    """

    def paginate(
        self, *, RegistryName: str, SchemaName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSchemaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListSchemaVersions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listschemaversionspaginator)
        """


class ListSchemasPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListSchemas)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listschemaspaginator)
    """

    def paginate(
        self,
        *,
        RegistryName: str,
        SchemaNamePrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.ListSchemas.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#listschemaspaginator)
        """


class SearchSchemasPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.SearchSchemas)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#searchschemaspaginator)
    """

    def paginate(
        self, *, Keywords: str, RegistryName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.18.53/reference/services/schemas.html#Schemas.Paginator.SearchSchemas.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_schemas/paginators.html#searchschemaspaginator)
        """
