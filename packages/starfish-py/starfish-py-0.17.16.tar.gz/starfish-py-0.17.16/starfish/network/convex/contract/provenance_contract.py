"""
    starfish.provenance contract

"""
import json

from convex_api.contract import Contract

from convex_api.utils import (
    add_0x_prefix,
    to_address
)


from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.did import (
    did_to_asset_id,
    did_to_id,
    is_asset_did
)
from starfish.types import AccountAddress


class ProvenanceContract(Contract):

    def register(self, asset_did: str, data: str, account: ConvexAccount):
        if not is_asset_did(asset_did):
            raise TypeError(f'{asset_did} is not an asset_did')
        did_id = add_0x_prefix(did_to_id(asset_did))
        asset_id = add_0x_prefix(did_to_asset_id(asset_did))
        quote_data = Contract.escape_string(data)
        command = f'(register {did_id} {asset_id} "{quote_data}")'
        result = self.send(command, account)
        if result and 'value' in result:
            return {
                'timestamp': result['value']['timestamp'],
                'owner': to_address(result['value']['owner']),
                'asset_id': asset_id,
                'did_id': did_id,
                'data': quote_data,
            }
        return result

    def get_data(self, asset_did: str, query_address: AccountAddress = None):
        if not is_asset_did(asset_did):
            raise TypeError(f'{asset_did} is not an asset_did')
        did_id = add_0x_prefix(did_to_id(asset_did))
        asset_id = add_0x_prefix(did_to_asset_id(asset_did))
        command = f'(get-data {did_id} {asset_id})'
        address = self.address
        if query_address:
            address = to_address(query_address)
        result = self.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result

    def did_id_list(self, did_id: str, query_address: AccountAddress = None):

        command = f'(did-id-list {add_0x_prefix(did_id)})'
        address = self.address
        if query_address:
            address = to_address(query_address)
        result = self.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result

    def owner_list(self, owner_address: AccountAddress, query_address: AccountAddress = None):
        query_address_value = self.address
        if query_address:
            query_address_value = to_address(query_address)

        owner_address_value = to_address(owner_address)
        command = f'(owner-list {owner_address_value})'
        result = self.query(command, query_address_value)
        if result and 'value' in result:
            return result['value']
        return result

    @staticmethod
    def convert_event_list(items):
        event_list = []
        if items is None:
            return event_list
        for item in items:
            json_data = item['data']
            try:
                json_data = json.loads(item['data'])
            except Exception as e:
                assert e
                pass
            event_list.append({
                'timestamp': item['timestamp'],
                'owner': to_address(item['owner']),
                'data': json_data,
            })
        return event_list
