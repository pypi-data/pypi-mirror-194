"""


    Contract Manager for Convex contracts


"""
import importlib
import inspect

from typing import Any

from convex_api import API
from convex_api.contract import Contract

from starfish.exceptions import StarfishContractError


class ContractManager:

    def __init__(self, convex: API,  default_package_name: str):
        self._convex = convex
        self._default_package_name = default_package_name

    def load(self, name: str, contract_name: str, package_name: str = None) -> Contract:
        """

        Load a contract using it's name, and network name

        :param str name: Name of the contract to load
        :param str artifact_filename: Optional filename of the artifact file
        :param bool has_artifact: Defaults to True, if false then just load the contract without an abi & address
        :param str package_name: Defaults to default_package_name, the package for the contract module

        :return: Return a contract object, else return None

        """
        if package_name is None:
            package_name = self._default_package_name
        if package_name is None:
            raise ValueError('You need to provide a package name for the contract classes')

        package_module = importlib.import_module(package_name)
        for item in inspect.getmembers(package_module, inspect.ismodule):
            class_def = ContractManager._find_class_in_module(name, item[1])
            if class_def:
                contract_object = class_def(self._convex)
                address = contract_object.load(contract_name)
                if not address:
                    raise StarfishContractError(f'cannot find contract for {contract_name}')
                return contract_object
        raise StarfishContractError(f'cannot find contract {name}')

    @staticmethod
    def _find_class_in_module(class_name: str, contract_module: str) -> Any:
        for name, obj in inspect.getmembers(contract_module, inspect.isclass):
            if issubclass(obj, Contract) \
               and name != 'Contract' \
               and name == class_name:
                return obj
        return None
