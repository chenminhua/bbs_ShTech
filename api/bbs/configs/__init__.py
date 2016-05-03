__author__ = 'chenminhua'
import datetime

TOKEN_EXPIRATION = datetime.datetime.utcnow() + datetime.timedelta(days=30)

TOKEN_SECRET = "it's a secret"

REDIS_EXPIRATION = 60 * 60 * 24 * 30

TOPICS_IN_EVERYPAGE = 40

USERS_IN_EVERYPAGE = 40

SEARCH_RESULT_IN_EVERYPAGE = 40

SMTP_CONFIG = { 'SMTPserver':'smtp.163.com', 'sender':'15651086913@163.com', 'password':'xujiu0413' }

administrator = ['sty']