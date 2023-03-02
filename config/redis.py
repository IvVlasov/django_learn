import redis
from django.conf import settings


redis_db = redis.StrictRedis(host=settings.REDIS_DATABASE['HOSTNAME'],
                             port=settings.REDIS_DATABASE['PORT'],
                             db=0,
                             charset="utf-8",
                             decode_responses=True)
