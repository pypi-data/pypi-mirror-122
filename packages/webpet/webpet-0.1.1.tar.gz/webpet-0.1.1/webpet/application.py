from webpet.exceptions.handler import handler
from webpet.request.HttpRequest import HTTPRequest
from webpet.conf import Configuration


class ASGIApplication():
    """Base class to asgi application
    """

    def __init__(self):
        """initiate ASGI Applitaction Instance of webpet

        Args:
            configuration (dict, optional): dict with configuration.
            Defaults to {}.
        """

    async def __call__(self, scope, receive, send):
        config = Configuration()
        if scope['type'] == 'http':
            body = await receive()
            request = HTTPRequest(scope, body['body'])

            if getattr(config, 'router', None) is None:
                if request.path != '/':
                    await send({
                        "type": "http.response.start",
                        "status": 307,
                        "headers": [(b'Location', b'/')],
                    })
                    await send({
                        "type": "http.response.body",
                        "body": ""
                    })
                else:
                    await send({
                        "type": "http.response.start",
                        "status": 200,
                        "headers": [(b"Content-type", b"text/html")]
                    })
                    await send({
                        "type": "http.response.body",
                        "body": b"<h1> Hello! </h1> <p> Async Rest framework installed successfully! <br> Please, go to docs for further configuration </p>"
                    })
            else:
                await handler(request, send)