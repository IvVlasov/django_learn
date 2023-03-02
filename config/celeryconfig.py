import json
from kombu.serialization import register
from django.conf import settings


class CustomEncoder(json.JSONEncoder):
    """Celery serialization"""

    def default(self, obj):
        return json.JSONEncoder.default(self, obj)


def custom_decoder(obj):
    return obj


# Encoder function
def custom_dumps(obj):
    return json.dumps(obj, cls=CustomEncoder, ensure_ascii=False)


# Decoder function
def custom_loads(obj):
    return json.loads(obj, object_hook=custom_decoder)


register(
    "custom_json",
    custom_dumps,
    custom_loads,
    content_type="application/x-custom_json",
    content_encoding="utf-8",
)

CELERY_BROKER_URL = f"redis://{settings.REDIS_DATABASE['HOSTNAME']}:\
    {settings.REDIS_DATABASE['PORT']}"
result_backend = "django-db"
result_extended = True

accept_content = ["custom_json"]
task_serializer = "custom_json"
result_serializer = "custom_json"
worker_state_db = "django-db"
