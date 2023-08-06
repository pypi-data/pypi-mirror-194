from orwynn.base.error import Error
from orwynn.base.exchandler._ExceptionHandler import ExceptionHandler
from orwynn.websocket._Websocket import Websocket


class DefaultWebsocketErrorHandler(ExceptionHandler):
    E = Error

    async def handle(self, request: Websocket, error: Error) -> None:
        await request.send_json(error.api)
