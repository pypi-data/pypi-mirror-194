"""
Type annotations for pricing service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing/type_defs/)

Usage::

    ```python
    from mypy_boto3_pricing.type_defs import AttributeValueTypeDef

    data: AttributeValueTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AttributeValueTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeServicesRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceTypeDef",
    "FilterTypeDef",
    "GetAttributeValuesRequestRequestTypeDef",
    "GetPriceListFileUrlRequestRequestTypeDef",
    "ListPriceListsRequestRequestTypeDef",
    "PriceListTypeDef",
    "DescribeServicesRequestDescribeServicesPaginateTypeDef",
    "GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef",
    "ListPriceListsRequestListPriceListsPaginateTypeDef",
    "GetAttributeValuesResponseTypeDef",
    "GetPriceListFileUrlResponseTypeDef",
    "GetProductsResponseTypeDef",
    "DescribeServicesResponseTypeDef",
    "GetProductsRequestGetProductsPaginateTypeDef",
    "GetProductsRequestRequestTypeDef",
    "ListPriceListsResponseTypeDef",
)

AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "Value": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

DescribeServicesRequestRequestTypeDef = TypedDict(
    "DescribeServicesRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "FormatVersion": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredServiceTypeDef = TypedDict(
    "_RequiredServiceTypeDef",
    {
        "ServiceCode": str,
    },
)
_OptionalServiceTypeDef = TypedDict(
    "_OptionalServiceTypeDef",
    {
        "AttributeNames": List[str],
    },
    total=False,
)


class ServiceTypeDef(_RequiredServiceTypeDef, _OptionalServiceTypeDef):
    pass


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Type": Literal["TERM_MATCH"],
        "Field": str,
        "Value": str,
    },
)

_RequiredGetAttributeValuesRequestRequestTypeDef = TypedDict(
    "_RequiredGetAttributeValuesRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "AttributeName": str,
    },
)
_OptionalGetAttributeValuesRequestRequestTypeDef = TypedDict(
    "_OptionalGetAttributeValuesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetAttributeValuesRequestRequestTypeDef(
    _RequiredGetAttributeValuesRequestRequestTypeDef,
    _OptionalGetAttributeValuesRequestRequestTypeDef,
):
    pass


GetPriceListFileUrlRequestRequestTypeDef = TypedDict(
    "GetPriceListFileUrlRequestRequestTypeDef",
    {
        "PriceListArn": str,
        "FileFormat": str,
    },
)

_RequiredListPriceListsRequestRequestTypeDef = TypedDict(
    "_RequiredListPriceListsRequestRequestTypeDef",
    {
        "ServiceCode": str,
        "EffectiveDate": Union[datetime, str],
        "CurrencyCode": str,
    },
)
_OptionalListPriceListsRequestRequestTypeDef = TypedDict(
    "_OptionalListPriceListsRequestRequestTypeDef",
    {
        "RegionCode": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListPriceListsRequestRequestTypeDef(
    _RequiredListPriceListsRequestRequestTypeDef, _OptionalListPriceListsRequestRequestTypeDef
):
    pass


PriceListTypeDef = TypedDict(
    "PriceListTypeDef",
    {
        "PriceListArn": str,
        "RegionCode": str,
        "CurrencyCode": str,
        "FileFormats": List[str],
    },
    total=False,
)

DescribeServicesRequestDescribeServicesPaginateTypeDef = TypedDict(
    "DescribeServicesRequestDescribeServicesPaginateTypeDef",
    {
        "ServiceCode": str,
        "FormatVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef = TypedDict(
    "_RequiredGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef",
    {
        "ServiceCode": str,
        "AttributeName": str,
    },
)
_OptionalGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef = TypedDict(
    "_OptionalGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetAttributeValuesRequestGetAttributeValuesPaginateTypeDef(
    _RequiredGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef,
    _OptionalGetAttributeValuesRequestGetAttributeValuesPaginateTypeDef,
):
    pass


_RequiredListPriceListsRequestListPriceListsPaginateTypeDef = TypedDict(
    "_RequiredListPriceListsRequestListPriceListsPaginateTypeDef",
    {
        "ServiceCode": str,
        "EffectiveDate": Union[datetime, str],
        "CurrencyCode": str,
    },
)
_OptionalListPriceListsRequestListPriceListsPaginateTypeDef = TypedDict(
    "_OptionalListPriceListsRequestListPriceListsPaginateTypeDef",
    {
        "RegionCode": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListPriceListsRequestListPriceListsPaginateTypeDef(
    _RequiredListPriceListsRequestListPriceListsPaginateTypeDef,
    _OptionalListPriceListsRequestListPriceListsPaginateTypeDef,
):
    pass


GetAttributeValuesResponseTypeDef = TypedDict(
    "GetAttributeValuesResponseTypeDef",
    {
        "AttributeValues": List[AttributeValueTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPriceListFileUrlResponseTypeDef = TypedDict(
    "GetPriceListFileUrlResponseTypeDef",
    {
        "Url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetProductsResponseTypeDef = TypedDict(
    "GetProductsResponseTypeDef",
    {
        "FormatVersion": str,
        "PriceList": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeServicesResponseTypeDef = TypedDict(
    "DescribeServicesResponseTypeDef",
    {
        "Services": List[ServiceTypeDef],
        "FormatVersion": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetProductsRequestGetProductsPaginateTypeDef = TypedDict(
    "_RequiredGetProductsRequestGetProductsPaginateTypeDef",
    {
        "ServiceCode": str,
    },
)
_OptionalGetProductsRequestGetProductsPaginateTypeDef = TypedDict(
    "_OptionalGetProductsRequestGetProductsPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "FormatVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetProductsRequestGetProductsPaginateTypeDef(
    _RequiredGetProductsRequestGetProductsPaginateTypeDef,
    _OptionalGetProductsRequestGetProductsPaginateTypeDef,
):
    pass


_RequiredGetProductsRequestRequestTypeDef = TypedDict(
    "_RequiredGetProductsRequestRequestTypeDef",
    {
        "ServiceCode": str,
    },
)
_OptionalGetProductsRequestRequestTypeDef = TypedDict(
    "_OptionalGetProductsRequestRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "FormatVersion": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetProductsRequestRequestTypeDef(
    _RequiredGetProductsRequestRequestTypeDef, _OptionalGetProductsRequestRequestTypeDef
):
    pass


ListPriceListsResponseTypeDef = TypedDict(
    "ListPriceListsResponseTypeDef",
    {
        "PriceLists": List[PriceListTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
