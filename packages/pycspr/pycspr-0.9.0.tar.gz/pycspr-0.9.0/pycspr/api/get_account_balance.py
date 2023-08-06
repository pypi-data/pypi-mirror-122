import typing

from pycspr import types
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    purse_uref: typing.Union[str, types.UnforgeableReference],
    state_root_hash: typing.Union[bytes, str] = None
    ) -> typing.Union[int, dict]:
    """Returns account balance at a certain state root hash.

    :param node: Encapsulates interaction with a remote node.
    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Account balance if on-chain account is found.

    """
    params = get_params(purse_uref, state_root_hash)
    response = node.get_response(constants.RPC_STATE_GET_BALANCE, params)

    return int(response["balance_value"])


def get_params(
    purse_uref: typing.Union[str, types.UnforgeableReference],
    state_root_hash: typing.Union[bytes, str] = None
    ) -> dict:
    """Returns JSON-RPC API request parameters.

    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(purse_uref, types.UnforgeableReference):
        purse_uref = purse_uref.as_string()
    if isinstance(state_root_hash, bytes):
        state_root_hash = state_root_hash.hex()

    return {
        "purse_uref": purse_uref,
        "state_root_hash": state_root_hash
    }
