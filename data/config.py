import os
import urllib.parse
from pathlib import Path

import environ
import pymongo
from aioredis import Redis

env = environ.Env()
environ.Env.read_env(env.str('ENV_PATH', '.env'))


# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = os.path.join(BASE_DIR, 'locales')


# BOT
BOT_TOKEN = env('BOT_TOKEN')
DOMAIN = 'API_SWIPE'


# root url for api
API_URL = env('API_URL')


# Database MongoDB
MONGO_CLIENT = pymongo.MongoClient(env('MONGO_CLIENT'))
MONGO_DB = MONGO_CLIENT[env('MONGO_INITDB_DATABASE')]
USERS_COLLECTION = MONGO_DB['users']

# Redis
REDIS_STORAGE = Redis(host='redis', decode_responses=True)





