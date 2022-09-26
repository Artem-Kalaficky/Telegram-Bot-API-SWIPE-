import os
from pathlib import Path

import environ
import pymongo

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
MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
MONGO_DB = MONGO_CLIENT['test']
USERS_COLLECTION = MONGO_DB['users']





