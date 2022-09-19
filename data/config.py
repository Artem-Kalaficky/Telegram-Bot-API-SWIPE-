import environ


env = environ.Env()
environ.Env.read_env(env.str('ENV_PATH', '.env'))


BOT_TOKEN = env('BOT_TOKEN')
