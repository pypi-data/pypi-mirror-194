from elm_framework_helpers.websockets.models.enhanced_websocket import EnhancedWebsocket
from elm_framework_helpers.websockets.models.message_types import MessageTypes
from elm_framework_helpers.websockets.models.status import Status


WebsocketBundle = tuple[
    EnhancedWebsocket, MessageTypes, Status | dict
]
WebsocketStatusBundle = tuple[EnhancedWebsocket, MessageTypes, Status]
WebsocketMessageBundle = tuple[
    EnhancedWebsocket, MessageTypes, dict
]
