from environs import Env

env = Env()
env.read_env()

DJANGO_SECRET_KEY = env.str('SECRET_KEY')
DJANGO_DEBUG = env.bool('DEBUG', default=True)
DJANGO_ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

ADMINS = env.list('ADMINS')
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

POSTGRES_DB = env.str('POSTGRES_DB')
POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
POSTGRES_HOST = env.str('POSTGRES_HOST')
POSTGRES_PORT = env.str('POSTGRES_PORT')
