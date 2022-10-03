import asyncio

import aiohttp
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
                    json = await resp.json()
                    USERS_COLLECTION.update_one(
                        {'user_id': self.user_id}, {'$set': {'access_token': json['access']}}, upsert=True
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
            telephone_form = mpwriter.append(profile['telephone'])
            telephone_form.set_content_disposition('attachment', name='telephone')

        client = await self.get_client(user_id, 'PUT', 'profile/change_my_contacts', data=mpwriter, headers=mpwriter.headers, is_multipart=True)
        response = await client.send_request()
        return True if response else None

    @staticmethod
    async def get_client(user_id, method, path, data=None, headers=None, is_multipart=False):
        client = BaseAPIClient(user_id, method, path, data, headers, is_multipart)
        return client





# url = URL(API_URL)
# async def main():
#
#     # headers = {
#     #     'content-type': 'application/x-www-form-urlencoded',
#     #     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0OTAyMzc2LCJpYXQiOjE2NjQ4MTU5NzYsImp0aSI6IjkyNzEwYTY1N2UzODRmYjc4ZTJkZDkyMjhhZjRjZGVhIiwidXNlcl9pZCI6MTN9.kekomO-EdD2GbrqaGcxbHPSmT0P_Rddq2JwsQUrMC0w'
#     # }
#     json = {'email': 'test1@gmail.com', 'password': 'Zaqwerty123'}
#
#
#     # with aiohttp.MultipartWriter('form-data') as mpwriter:
#     #     part = mpwriter.append('test1@gmail.com')
#     #     part.set_content_disposition('form-data', name='email')
#     #
#     #     part = mpwriter.append('Карпов')
#     #     part.set_content_disposition('attachment', name='last_name')
#     #
#     #     mpwriter.headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0OTAzOTA0LCJpYXQiOjE2NjQ4MTc1MDQsImp0aSI6IjQxM2VjMTliNDQ4NjQxNmY4MWY1MDZlODgxNGVmMzk3IiwidXNlcl9pZCI6MTN9.00RS7KEMUSyYdP1xAvtI_njLV8_qB6ISBPrzqLff7Dc'
#     #
#     async with aiohttp.ClientSession(headers=None) as session:
#         async with session.request('POST', url.with_path('/account/login/'), data=json) as resp:
#             print(resp.status)
#             print(resp.headers)
#             print(await resp.text())
#
#
# asyncio.run(main())










# class BaseAPIClient:
#     url = URL(API_URL)
#
#     async def send_request(self, user_id, method, path, data=None, headers=None):
#         if headers:
#             headers = await self.get_headers(user_id)
#
#         async with aiohttp.ClientSession(headers=headers) as session:
#             async with session.request(method, self.url.with_path(path), json=data) as resp:
#                 if resp.status == 200 or resp.status == 201:
#                     response_json = await resp.json()
#                     return response_json
#                 else:
#                     await self.request_error(resp.status, user_id)
#
#     async def get_headers(self, user_id):
#         user = await self.get_user(user_id)
#         headers = {
#             'content-type': 'application/json',
#             'Authorization': f'Bearer {user["access_token"]}' # noqa
#         }
#         return headers
#
#     async def request_error(self, status, user_id):
#         if status == 400:
#             return None
#         if status == 401:
#             await self.get_token(user_id)
#
#     async def get_token(self, user_id):
#         user = await self.get_user(user_id)
#         data = {'refresh': user['refresh_token']}
#         async with aiohttp.ClientSession() as session:
#             async with session.post(self.url.with_path('/token/refresh/'), json=data) as resp:
#                 if resp.status == 200:
#                     await self.send_request(user_id)
#                 else:
#                     print(resp.status)
#                     print(await resp.text())
#
#     @staticmethod
#     async def get_user(user_id):
#         user = USERS_COLLECTION.find_one({'user_id': user_id})
#         return user
#
#
# class UserAPIClient(BaseAPIClient):
#     async def build_register_request(self, data):
#         response = await super().send_request(None, 'POST', '/account/register/', data)
#         return True if response else None
#
#     async def build_login_request(self, user_id, data):
#         response_json = await super().send_request(user_id, 'POST', '/account/login/', data)
#         if response_json:
#             user = {
#                 '$set': {
#                     'user_id': user_id,
#                     'access_token': response_json['access_token'],
#                     'refresh_token': response_json['refresh_token'],
#                     'is_authenticated': True
#                 }
#             }
#             USERS_COLLECTION.update_one({'user_id': user_id}, user, upsert=True)
#         return True if response_json else None
#
#     async def build_get_profile_request(self, user_id):
#         response = await super().send_request(user_id, 'GET', '/profile/my_profile/', headers=True)
#         return response if response else None