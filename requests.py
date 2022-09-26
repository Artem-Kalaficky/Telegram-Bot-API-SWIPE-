import asyncio

import aiohttp
from yarl import URL

from data.config import API_URL, USERS_COLLECTION


class BaseAPIClient:
    url = URL(API_URL)

    async def send_request(self, user_id, method, path, data=None, headers=None):

        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.url.with_path(path), json=data, headers=headers) as resp:
                if resp.status == 200:
                    response_json = await resp.json()
                    user = {
                        '$set': {
                            'user_id': user_id,
                            'access_token': response_json['access_token'],
                            'refresh_token': response_json['refresh_token'],
                            'is_authenticated': True
                        }
                    }
                    USERS_COLLECTION.update_one({'user_id': user_id}, user, upsert=True)
                    return resp
                if resp.status == 201:
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
        response = await super().send_request('POST', '/account/register/', data)
        return True if response else None

    async def build_login_request(self, user_id, data=None):
        response = await super().send_request(user_id, 'POST', '/account/login/', data)
        if response:
            return True
        else:
            return False



