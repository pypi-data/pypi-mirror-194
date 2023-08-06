from logging import getLogger
from typing import Any, cast
from reactivex.subject import BehaviorSubject
import reactivex

import orjson
import websocket


logger = getLogger(__name__)
raw_logger = getLogger("elm_framework_helpers.raw_socket.sent")


class EnhancedWebsocket:
    socket: websocket.WebSocketApp
    _id = 0

    def __str__(self):
        return f"EnhancedWebsocket <{self.socket.url}>"

    def __init__(self, socket: websocket.WebSocketApp):
        self.socket = socket

    def send_message(self, message: Any) -> int | str:
        raise NotImplementedError(
            "send_message needs to be implemented in enhanced websocket"
        )

    def prepare_request(self, message: Any) -> tuple[int | str, bytes]:
        raise NotImplementedError(
            "prepare_request needs to be implemented in enhanced websocket"
        )

    def request_to_observable(
        self, message: dict
    ) -> tuple[int, reactivex.Observable[Any]]:
        message_id, as_bytes = self.prepare_request(message)

        def send_():
            logger.debug("[SOCKET][BYTES] Sending json to socket: %s", as_bytes)
            raw_logger.debug(as_bytes.decode())
            self.socket.send(as_bytes)

        return message_id, reactivex.from_callable(send_)

    def send_json(self, message: Any):
        message_id, as_bytes = self.prepare_request(message)
        logger.debug("[SOCKET] Sending json to socket: %s", as_bytes)
        raw_logger.debug(as_bytes.decode())
        self.socket.send(as_bytes)
        return message_id


EnhancedWebsocketBehaviorSubject = BehaviorSubject[EnhancedWebsocket]

__all__ = [
    "EnhancedWebsocket",
    "EnhancedWebsocketBehaviorSubject",
]
