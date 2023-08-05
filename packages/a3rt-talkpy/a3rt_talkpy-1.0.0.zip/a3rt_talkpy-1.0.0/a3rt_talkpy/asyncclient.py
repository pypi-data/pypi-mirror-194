import aiohttp

from .response import Response
from .exception import *

class AsyncTalkClient:
    def __init__(self, apikey: str) -> None:
        self.apikey: str = apikey
        self.base_url: str = 'https://api.a3rt.recruit.co.jp/talk/v1/smalltalk'

    async def talk(self, query: str) -> Response:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, data={'apikey': self.apikey, 'query': query}) as res:
                response = await res.json()
                match response['status']:
                    case 0:
                        return Response(response=response)
                    case 1000:
                        raise ApiKeyIsNull
                    case 1001:
                        raise ApiKeyNotFound
                    case 1002:
                        raise DeletedAccount
                    case 1003:
                        raise TemporaryAccount
                    case 1010:
                        raise ServerNotFound
                    case 1011:
                        raise ServerParameterError
                    case 1030:
                        raise AccessDeny
                    case 1400:
                        raise BadRequest
                    case 1404:
                        raise NotFound
                    case 1405:
                        raise MethodNotAllowed
                    case 1413:
                        raise RequestEntityTooLong
                    case 1500:
                        raise InternalServerError
                    case 2000:
                        return Response(response=response)
                    case _:
                        raise UnknownError
