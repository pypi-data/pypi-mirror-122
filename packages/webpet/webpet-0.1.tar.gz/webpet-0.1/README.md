# Webpet

Simple async web framework for python

This is my pet project and it doesn't pretend to be serious

## Links

- [Views](webpet/views/README.md)
- [Routers](webpet/routers/README.md)
- [Exceptions](webpet/exceptions/README.md)
- [Requests](webpet/request/README.md)

## Simple Usage example

```python
from webpet.application import ASGIApplication
from webpet.response import HTTPResponse
from webpet.routers import HTTPRouter, URL
from webpet.views import View, LongPoolView

import asyncio
import json
import random

class Index(View):

    async def get(self):
        await self.send(
            HTTPResponse(
                '<h1> Hello World </h1>',
                content_type='text/html'
            )
        )


class Aboba(View):

    async def get(self):
        await self.send(
            HTTPResponse(
                '<h1> Aboba </h1>',
                content_type='text/html'
            )
        )


class TestLong(LongPoolView):

    async def get(self):
        await self.open(status_code=200, headers=[(b'Content-type', b'application/json')])
        data = []
        ticks = 0
        while True:
            ticks += 1
            number = random.randint(0, 1000)
            data.append(number)
            if number >= 500:
                await self.send(HTTPResponse(
                    json.dumps({
                        'data': data,
                        'ticks': ticks
                    })
                ))
                break
            else:
                await asyncio.sleep(1)


router = HTTPRouter(routes=[
    URL('/', Index),
    URL('/another', Aboba),
    URL('/longpool', TestLong)
])

app = ASGIApplication({
    'router': router
})
```

### **To run with daphne use**

```bash
pip install daphne
daphne <application_name>:<ASGIApplication instance>
```
