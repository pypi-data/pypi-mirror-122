import typing

from pycspr import crypto
from pycspr import factory
from pycspr import types
from pycspr.client import NodeConnectionInfo
from pycspr.api.get_account_info import execute as get_account_info



def execute(
    node: NodeConnectionInfo,
    account_key: typing.Union[bytes, str],
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> types.UnforgeableReference:
    """Returns an on-chain account's main purse unforgeable reference.

    :param node: Information required to connect to a node.
    :param account_key: Key of an on-chain account.
    :param block_id: Identifier of a finalised block.
    :returns: Account main purse unforgeable reference.

    """
    account_info = get_account_info(node, account_key, block_id)

    return factory.create_uref_from_string(account_info["main_purse"])
