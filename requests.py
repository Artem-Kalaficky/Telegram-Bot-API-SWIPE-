import asyncio

import aiohttp
from yarl import URL

from data.config import API_URL


class BaseAPIClient:
    url = URL(API_URL)

    async def send_request(self, method, path, data=None, headers=None):

        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.url.with_path(path), json=data, headers=headers) as resp:
                if resp.status == 200 or resp.status == 201:
                    return resp
                else:
                    await self.request_error(resp)

    async def request_error(self, response):
        if response.status == 400:
            return response
        if response.status == 401:
            pass
        if response.status == 403:
            pass


class UserAPIClient(BaseAPIClient):
    async def build_register_request(self, data=None):
        json = {
            'email': data['email'],
            'password1': data['password1'],
            'password2': data['password2'],
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }
        response = await super().send_request('POST', '/account/register/', json)
        return True if response else None



# url = URL(API_URL)
# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.request('POST', url.with_path('/account/login/'), json={'email': 'admin@gmail.com', 'password': 'Zaqwerty123'}) as resp:
#             print(resp.status)
#             print(await resp.text())
#
# asyncio.run(main())


