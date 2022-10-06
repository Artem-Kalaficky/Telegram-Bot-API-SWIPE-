import json

import aiohttp
from aiohttp import payload
from yarl import URL

from data.config import API_URL, USERS_COLLECTION


class BaseAPIClient:
    url = URL(API_URL)

    def __init__(self, user_id, method, path, data=None, headers=None, is_multipart=False):
        self.user_id = user_id
        self.method = method
        self.path = path
        self.data = data
        self.headers = headers
        self.is_multipart = is_multipart

    async def get_user(self):
        user = USERS_COLLECTION.find_one({'user_id': self.user_id})
        return user

    async def get_headers(self):
        user = await self.get_user()
        if not self.is_multipart:
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {user["access_token"]}'
            }
        else:
            self.headers['Authorization'] = f'Bearer {user["access_token"]}'
            headers = self.headers
        return headers

    async def send_request(self):
        if self.headers:
            self.headers = await self.get_headers()

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.request(self.method, self.url.with_path(self.path), data=self.data) as resp:
                if resp.status == 200 or resp.status == 201:
                    response_json = await resp.json()
                    return response_json
                else:
                    response_json = await self.request_error(resp.status)
                    return response_json

    async def request_error(self, status):
        if status == 400:
            return None
        if status == 401:
            response_json = await self.get_token()
            return response_json

    async def get_token(self):
        user = await self.get_user()
        data = {'refresh': user['refresh_token']}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url.with_path('/token/refresh/'), json=data) as resp:
                if resp.status == 200:
                    resp_json = await resp.json()
                    USERS_COLLECTION.update_one(
                        {'user_id': self.user_id}, {'$set': {'access_token': resp_json['access']}}, upsert=True
                    )
                    response_json = await self.send_request()
                    return response_json
                else:
                    return None


class UserAPIClient:
    async def build_register_request(self, data):
        client = await self.get_client(None, 'POST', '/account/register/', data)
        response = await client.send_request()
        return True if response else None

    async def build_login_request(self, user_id, data):
        client = await self.get_client(user_id, 'POST', '/account/login/', data)
        response_json = await client.send_request()
        if response_json:
            user = {
                '$set': {
                    'user_id': user_id,
                    'access_token': response_json['access_token'],
                    'refresh_token': response_json['refresh_token'],
                    'is_authenticated': True
                }
            }
            USERS_COLLECTION.update_one({'user_id': user_id}, user, upsert=True)
        return True if response_json else None

    async def build_get_profile_request(self, user_id):
        client = await self.get_client(user_id, 'GET', '/profile/my_profile/', headers=True)
        response = await client.send_request()
        return response if response else None

    async def build_get_my_ads_request(self, user_id):
        client = await self.get_client(user_id, 'GET', '/ads/my-ads/', headers=True)
        response = await client.send_request()
        return response if response else None

    async def build_update_profile_request(self, user_id, profile):
        with aiohttp.MultipartWriter('form-data') as mpwriter:
            email_form = mpwriter.append(profile['email'])
            email_form.set_content_disposition('form-data', name='email')
            last_name_form = mpwriter.append(profile['last_name'])
            last_name_form.set_content_disposition('attachment', name='last_name')
            first_name_form = mpwriter.append(profile['first_name'])
            first_name_form.set_content_disposition('attachment', name='first_name')
            if profile['telephone']:
                telephone_form = mpwriter.append(profile['telephone'])
                telephone_form.set_content_disposition('attachment', name='telephone')
            if isinstance(profile['avatar'], type(b'')):
                avatar_form = mpwriter.append(profile['avatar'])
                avatar_form.set_content_disposition('attachment', name='avatar', filename='avatar.jpeg')
        client = await self.get_client(
            user_id, 'PUT', 'profile/change_my_contacts', data=mpwriter, headers=mpwriter.headers, is_multipart=True
        )
        response = await client.send_request()
        return True if response else None

    async def build_get_feed_request(self, user_id):
        client = await self.get_client(user_id, 'GET', '/feed/', headers=True)
        response = await client.send_request()
        return response if response else None

    async def build_create_ad_request(self, user_id, data):
        serialize_data = payload.JsonPayload(data, dumps=json.dumps)
        client = await self.get_client(user_id, 'POST', '/ads/my-ads/', data=serialize_data, headers=True)
        response = await client.send_request()
        return response if response else None

    async def build_get_ad_request(self, user_id, ad_id):
        client = await self.get_client(user_id, 'GET', f'/ads/my-ads/{ad_id}/', headers=True)
        response = await client.send_request()
        return response if response else None

    async def build_update_ad_request(self, user_id, ad_id, data):
        serialize_data = payload.JsonPayload(data, dumps=json.dumps)
        client = await self.get_client(
            user_id, 'PUT', f'/ads/my-ads/{ad_id}/update_ad/', data=serialize_data, headers=True
        )
        response = await client.send_request()
        return response if response else None

    @staticmethod
    async def get_client(user_id, method, path, data=None, headers=None, is_multipart=False):
        client = BaseAPIClient(user_id, method, path, data, headers, is_multipart)
        return client
