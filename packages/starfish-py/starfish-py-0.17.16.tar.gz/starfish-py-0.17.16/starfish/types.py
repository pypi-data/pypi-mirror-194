"""

    Types used for typing


"""
import sys

from datetime import datetime
from typing import (
    Any,
    List,
    Tuple,
    TypeVar,
    Union
)

# TypeDict is only available in python3.8
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

TAccountBase = TypeVar('AccountBase')
TAsset = TypeVar('Asset')
TAssetBase = TypeVar('AssetBase')
TBundleAsset = TypeVar('BundleAsset')
TDataAsset = TypeVar('DataAsset')
TOperationAsset = TypeVar('OperationAsset')
TRemoteDataAsset = TypeVar('RemoteDataAsset')
TContractManager = TypeVar('ContractManager')
TDDO = TypeVar('DDO')
TJob = TypeVar('Job')
TListing = TypeVar('Listing')
TListingBase = TypeVar('ListingBase')
TNetworkBase = TypeVar('NetworkBase')
TRemoteAgent = TypeVar('RemoteAgent')
TAuthentication = TypeVar('Authentication')


class AccountInitParams(TypedDict):
    address: str
    password: str
    key_value: Any
    key_file: str


class AgentItem(TypedDict):
    url: str
    did: str
    authentication: TAuthentication


class DIDParts(TypedDict):
    method: str
    id: str
    path: str
    fragment: str
    id_hex: str


class ProvenanceEvent(TypedDict):
    asset_id: str
    account: str
    timestamp: datetime


class ListingData(TypedDict):
    trust_level: int
    userid: str
    assetid: str
    agreement: str
    ctime: str
    status: str
    id: str
    info: Any
    utime: str


AccountAddressOrDict = Union[AccountInitParams, str, Tuple[str, str, str]]

AccountAddress = Union[TAccountBase, str, int]

ProvenanceEventList = List[ProvenanceEvent]
