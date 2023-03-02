from celery import shared_task
from .services.parser import parse_all
from celery.exceptions import Ignore


@shared_task(name="Parser", bind=True)
def parse_all_task(self, categories: list[dict[str, str]]) -> str:
    self.update_state(state='STARTED', meta='Ожидайте выполнения')
    result = parse_all(categories)

    if result.get('code') == 'error':
        self.update_state(state='FAILURE', meta=result.get('message'))
        raise Ignore()

    return result.get('message')
