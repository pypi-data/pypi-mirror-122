import json
import typing

import requests
import sseclient

from pycspr.client.events import NodeConnectionInfo
from pycspr.client.events import NodeSseChannelType
from pycspr.client.events import NodeSseEventType


# Map: channel type <-> event type.
_CHANNEL_TO_TYPE = {
    NodeSseChannelType.deploys: {
        NodeSseEventType.ApiVersion,
        NodeSseEventType.DeployAccepted
    },
    NodeSseChannelType.main: {
        NodeSseEventType.ApiVersion,
        NodeSseEventType.BlockAdded,
        NodeSseEventType.DeployProcessed,
        NodeSseEventType.Fault,
        NodeSseEventType.Step
    },
    NodeSseChannelType.sigs: {
        NodeSseEventType.ApiVersion,
        NodeSseEventType.FinalitySignature
    }
}


def execute(
    node: NodeConnectionInfo,
    callback: typing.Callable,
    channel_type: NodeSseChannelType,
    event_type: NodeSseEventType = None,
    event_id: int = 0
    ):
    """Binds to a node's event stream - events are passed to callback for processing.

    :param node: Information required to connect to a node.
    :param callback: Callback to invoke whenever an event of relevant type is received.
    :param channel_type: Type of event channel to which to bind.
    :param event_type: Type of event type to listen for (all if unspecified).
    :param event_id: Identifer of event from which to start stream listening.

    """
    if event_type is not None:
        _validate_that_channel_supports_event_type(channel_type, event_type)

    sse_client = _get_sse_client(node, channel_type, event_id)
    for event_type, event_id, payload in _yield_events(sse_client):
        callback(channel_type, event_type, event_id, payload)


def _get_sse_client(node: NodeConnectionInfo, channel_type: NodeSseChannelType, event_id: int):
    """Returns SSE client.

    """
    url = f"{node.address_sse}/{channel_type.name.lower()}"
    if event_id:
        url = f"{url}?start_from={event_id}"
    stream = requests.get(url, stream=True)

    return sseclient.SSEClient(stream)


def _parse_event(event_id: int, payload: dict) -> typing.Tuple[NodeSseEventType, int, dict]:
    """Parses raw event data for upstream processing.

    """
    if "ApiVersion" in payload:
        pass

    elif "BlockAdded" in payload:
        return \
            NodeSseEventType.BlockAdded, \
            event_id, \
            payload

    elif "DeployProcessed" in payload:
        return \
            NodeSseEventType.DeployProcessed, \
            event_id, \
            payload

    elif "Fault" in payload:
        return \
            NodeSseEventType.Fault, \
            event_id, \
            payload

    elif "Step" in payload:
        return \
            NodeSseEventType.Step, \
            event_id, \
            payload

    elif "DeployAccepted" in payload:
        return \
            NodeSseEventType.DeployAccepted, \
            event_id, \
            payload

    elif "FinalitySignature" in payload:
        return \
            NodeSseEventType.FinalitySignature, \
            event_id, \
            payload

    else:
        print("TODO: process unknown event: {payload}")


def _validate_that_channel_supports_event_type(channel_type: NodeSseChannelType, event_type: NodeSseEventType = None):
    """Validates that the channel supports the event type.

    """    
    if channel_type not in _CHANNEL_TO_TYPE:
        raise ValueError(f"Unsupported SSE channel: {channel_type.name}.")

    if event_type not in _CHANNEL_TO_TYPE[channel_type]:
        raise ValueError(f"Unsupported SSE channel/event permutation: {channel_type.name}:{event_type.name}.")


def _yield_events(sse_client) -> typing.Generator:
    """Yields events streaming from node.

    """
    try:
        for event in sse_client.events():
            parsed = _parse_event(event.id, json.loads(event.data))
            if parsed:
                yield parsed
    except Exception as err:
        try:
            sse_client.close()
        except:
            pass
        finally:
            raise err
