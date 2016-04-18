__author__ = 'chenminhua'
import datetime

TOKEN_EXPIRATION = datetime.datetime.utcnow() + datetime.timedelta(days=30)

TOKEN_SECRET = "it's a secret"

REDIS_EXPIRATION = 60 * 60 * 24 * 30