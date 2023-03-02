import random
from . mailing import send_confirm_code
from config.redis import redis_db


class CodeConfirm(object):

    def __init__(self, request, email=''):
        self.session = request.session
        self.email_confirm = self.session.get('email', email)
        code = redis_db.get(self.email_confirm)
        self.code = code

    def craete(self) -> None:
        if not self.code:
            self.code = random.randint(10000, 99999)
        self.save()

    def send_code_to_email(self) -> None:
        send_confirm_code(int(self.code), self.email_confirm)

    def check(self, form_code: str) -> bool:
        return int(self.code) == int(form_code)

    def clean(self) -> None:
        redis_db.delete(self.email_confirm)
        del self.session['email']
        self.session.modified = True

    def save(self) -> None:
        redis_db.set(self.email_confirm, self.code)
        self.session['email'] = self.email_confirm
        self.session.modified = True
