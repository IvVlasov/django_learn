import requests
import random
import string
import urllib.parse
from datetime import datetime, timedelta

from django.utils import dateparse
from django.conf import settings

from typing import Optional
from order.models import Order
from authentication.models import User
from config.redis import redis_db


class QiwiPayment:
    """
    Qiwi Api Docs
    https://developer.qiwi.com/ru/p2p-payments/#status
    """

    headers = { 
        'content-type': 'application/json',
        'accept': 'application/json',
        'Authorization': 'Bearer ' + settings.QIWI_SECRET_KEY,
    }
    api_url = 'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}'

    def __init__(self, user: User, order: Order):
        self.user_obj = user
        self.order_obj = order

    def create_payment_link(self) -> Optional[str]:
        data = {
            "amount": {
                "currency": "RUB",
                "value": f'{self.order_obj.amount:.2f}'
                },
            "expirationDateTime": self._generate_date_expirity(),
        }
        billid = self._write_bill_id()
        url = self.api_url.format(bill_id=billid)
        response = requests.put(url, headers=self.headers, json=data)
        if response.status_code == 200:
            json_response = response.json()
            success_url = f'{settings.BASE_URL}/cart/orders/{self.user_obj.id}'
            payUrl = json_response['payUrl'] + \
                '&successUrl=' + urllib.parse.quote(success_url)
            return payUrl

    def _write_bill_id(self) -> str:
        bill_id = self._generate_bill_id()
        bill_data = {self.order_obj.id: bill_id}
        redis_db.hmset('qiwi_' + self.user_obj.email, bill_data)
        return bill_id

    # Check pay
    def get_bill_id(self) -> Optional[str]:
        db_data = redis_db.hgetall('qiwi_' + self.user_obj.email)
        return db_data.get(str(self.order_obj.id))

    def get_qiwi_payment(self) -> Optional[dict]:
        bill_id = self.get_bill_id()
        url = self.api_url.format(bill_id=bill_id)
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            json_response = response.json()
            json_response['expirationDateTime'] = dateparse.parse_datetime(
                json_response['expirationDateTime']
            )
            return json_response

    @staticmethod
    def _generate_bill_id() -> str:
        simbols = string.ascii_letters + string.digits
        bill_id = ''.join(random.sample(simbols, settings.BILL_ID_LENGTH))
        return bill_id

    @staticmethod
    def _generate_date_expirity() -> str:
        date_expirity = datetime.now() + timedelta(minutes=60)
        date_expirity = date_expirity.strftime('%Y-%m-%dT%H:%M') + '+03:00'
        return date_expirity

    def clear_db(self) -> None:
        redis_db.hdel('qiwi_' + self.user_obj.email, self.order_obj.id)
