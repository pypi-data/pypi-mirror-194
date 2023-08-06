import asyncio
from typing import List, Union
from aiohttp_retry import RetryClient, ExponentialRetry
from aiohttp import ClientResponse
from aiohttp.streams import StreamReader
import requests

from .config import Configuration
from .exceptions import SDKError, ApiInvalidPayload, ApiAuthorizationError, ConfigurationError, RetarusRessourceNotFound
from .region import RegionUri, region_resolve


class Transporter:
    retry_options = ExponentialRetry(attempts=1)

    def __init__(self, uris):
        self.service_uri_regions: List[RegionUri] = uris

    async def post(self, path: str, payload: dict, query_parms: dict = {}):
        self.__validate_auth()
        region = region_resolve(Configuration.region, self.service_uri_regions)
        url = f"{region.ha_uri}/rest/v1{path}"
        async with RetryClient(retry_options=self.retry_options) as session:
            async with session.post(
                url=url, json=payload, headers=Configuration.auth, params=query_parms
            ) as resp:
                return await self.__match_response(resp)

    async def get(self, path: str, query_parms: dict = {}):
        self.__validate_auth()
        async with RetryClient(retry_options=self.retry_options) as session:

            @fetch_datacenter(regions=self.service_uri_regions)
            async def get(host: str):
                url = f"{host}/rest/v1/{path}"
                async with session.get(
                    url=url, headers=Configuration.auth, params=query_parms
                ) as resp:
                    return await self.__match_response(resp)

            return await get()

    async def delete(self, path: str):
        self.__validate_auth()
        async with RetryClient(retry_options=self.retry_options) as session:
            @fetch_datacenter(regions=self.service_uri_regions)
            async def delete(host: str):
                url = f"{host}/rest/v1/{path}"
                async with session.delete(url=url, headers=Configuration.auth) as resp:
                    return await self.__match_response(resp)

            return await delete()

    async def form_post(self, payload: dict):
        url = self.service_uri_regions[0].ha_uri
        resp = requests.post(url, files=payload)
        if resp.status_code == 200:
            print(resp.content)
            return None
        print(f"{resp.content}")
        raise SDKError(
            message="Check what the server responded above"
        )

    async def __match_response(self, resp: ClientResponse) -> Union[bool, dict, StreamReader]:

        if resp.status == 401 or resp.status == 403:
            raise ApiAuthorizationError()
        elif resp.status == 400:
            raise ApiInvalidPayload()
        elif resp.status == 404:
            return False
        elif resp.status == 200 or resp.status == 201:
            if resp.content_type == "text/plain":
                return resp.content
            if resp.content_type != "application/json":
                return await resp.content.read()
            data = await resp.json()
            return data
        print(f"An unexpected error occurred, there might be something wrong with the sdk.\n{resp.text}, Please contact the retarus support")
        raise SDKError(
            message=f"An unexpected error occurred, there might be something wrong with the sdk.\n  {resp.content}, Please contact the retarus support"
        )

    @staticmethod
    def __validate_auth():
        """
        Validates the global sdk configuration, if the required value are not set it will raise a ConfigurationError
        """
        if Configuration.auth == {}:
            raise ConfigurationError(
                message="You need to set the credentails using the set_auth() function in the Confugration class"
            )


def fetch_datacenter(regions: List[RegionUri]):
    """
    A decorator to iterate over a list of hostnames a check for a valid response.
    """
    uri = region_resolve(Configuration.region, regions)

    def wrap(func):
        async def wrapped(*args):
            counter = 0
            for server in uri.urls:
                res = await func(server)
                if res is False and counter < len(uri.urls):
                    counter += 1
                    continue
                if res is False:
                    raise RetarusRessourceNotFound()
                return res
            raise SDKError(message="No report found, there must be an issue with the sdk.")
        return wrapped

    return wrap

