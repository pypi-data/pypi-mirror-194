from typing import Callable, List, Optional, Tuple, cast

from reactivex import compose, operators, Observable
import reactivex

from elm_framework_helpers.websockets import models


ReadyMessage = Tuple[models.EnhancedWebsocket, bool]


def filter_socket_status_only() -> Callable[
    [Observable[models.WebsocketBundle]], Observable[models.WebsocketStatusBundle]
]:
    def is_status(x):
        return x[1] == models.WEBSOCKET_STATUS

    """Grab only messages related to the status of the websocket connection"""
    return compose(
        operators.filter(is_status),
        operators.map(lambda x: cast(models.WebsocketStatusBundle, x)),
    )


def map_socket_only() -> Callable[
    [Observable[models.WebsocketBundle | ReadyMessage]], Observable[models.EnhancedWebsocket]
]:
    """Returns an observable that represents the websocket only whenever emitted"""
    return operators.map(lambda x: x[0])


def _is_message(message: models.WebsocketBundle) -> bool:
    return message[1] == models.WEBSOCKET_MESSAGE


def message_only() -> Callable[
    [Observable[models.WebsocketBundle] | Observable[models.WebsocketStatusBundle]],
    Observable[models.Status | dict],
]:
    return operators.map(lambda x: x[2])


def keep_messages_only() -> Callable[
    [Observable[models.WebsocketBundle]], Observable[dict]
]:
    return compose(
        operators.filter(_is_message),
        message_only(),
    )


def keep_new_socket_only() -> Callable[
    [Observable[models.WebsocketBundle]], Observable[models.EnhancedWebsocket]
]:
    # TODO this extra 1 second is actually coming from Cryptodotcom; we should probably make it an argument to the function
    def wait(x: models.EnhancedWebsocket):
        return reactivex.timer(1.0).pipe(operators.map(lambda _: x))

    return compose(
        operators.map(lambda x: x[0]),
        operators.distinct_until_changed(),
        operators.map(wait),
        operators.switch_latest(),
    )
