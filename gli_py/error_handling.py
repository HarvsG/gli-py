from requests import Response
from json import loads
import asyncio
import uplink
class UnsuccessfulRequest(Exception):
    '''raised when the status code is not 200'''


class NonZeroResponse(Exception):
    '''raised when the router responds but with a non O code'''

class TokenError(Exception):
    '''raised when the router responds but with a -1 code'''


def raise_for_status(response: Response):
    """Checks whether or not the response was successful."""
    if 200 <= response.status < 300:
        # Pass through the response.
        res = loads(response.text())
        # Gl-inet's api uses its own error codes that are returned in
        # status 200 messages - this is out of spec so we must handle it
        if res['code'] == -1:
            raise TokenError("Request returned error code -1 (InvalidAuth), is the token expired or the passowrd wrong?")
        if res['code'] == -204:
            return res
        if res['code'] < 0:
            if 'msg' not in res:
                res['msg'] = "null"

            raise NonZeroResponse("Request returned error code %s with message:' %s'. Full response %s" % (res['code'], res['msg'],res))
        return res

    raise UnsuccessfulRequest(response.url)
