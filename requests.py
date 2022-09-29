import aiohttp
from yarl import URL

from data.config import API_URL, USERS_COLLECTION


class BaseAPIClient:
    url = URL(API_URL)

    def __init__(self, user_id, method, path, data=None, headers=None):
        self.user_id = user_id
        self.method = method
        self.path = path
        self.data = data
        self.headers = headers

    async def send_request(self):
        if self.headers:
            self.headers = await self.get_headers()

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.request(self.method, self.url.with_path(self.path), json=self.data) as resp:
                if resp.status == 200 or resp.status == 201:
                    response_json = await resp.json()
                    return response_json
                else:
                    await self.request_error(resp.status)

    async def get_headers(self):
        user = await self.get_user()
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {user["access_token"]}'
        }
        return headers

    async def get_user(self):
        user = USERS_COLLECTION.find_one({'user_id': self.user_id})
        return user

    async def request_error(self, status):
        if status == 400:
            return None
        if status == 401:
            await self.get_token()

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
                    await self.send_request()
                else:
                    print(resp.status)
                    print(await resp.text())


class UserAPIClient(BaseAPIClient):
    # async def build_register_request(self, data):
    #     client = await self.get_client(None, 'POST', '/account/register/', data)
    #     response = await client.send_request()
    #     return True if response else None

    async def build_login_request(self, user_id, data):
        super().__init__(user_id, 'POST', '/account/login/', data)
        response_json = await self.send_request()
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

    # async def build_get_profile_request(self, user_id):
    #     client = await self.get_client(user_id, 'GET', '/profile/my_profile/', headers=True)
    #     response = await client.send_request()
    #     return response if response else None

    # @staticmethod
    # async def get_client(user_id, method, path, data=None, headers=None):
    #     client = BaseAPIClient(user_id, method, path, data, headers)
    #     return client


# url = URL(API_URL)
# async def main():
#     data = None
#     headers = {
#         'content-type': 'application/json',
#         'Authorization': 'Bearer '
#     }
#     asd = USERS_COLLECTION.find_one({'user_id': 798507215})
#     print(asd)
#     print(asd['access_token'])
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.request('GET', url.with_path('/profile/my_profile/'), json=data) as resp:
#             print(resp.status)
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