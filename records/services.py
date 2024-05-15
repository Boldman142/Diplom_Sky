from core import settings
import requests


class DoneRecord:
    pass
    # URL = 'https://api.telegram.org/bot'
    # TOKEN = settings.TELEGRAM_TOKEN
    # chat_id = settings.TELEGRAM_ID
    #
    # def send_message(self, text):
    #     requests.post(
    #         url=f'{self.URL}{self.TOKEN}/sendMessage',
    #         data={
    #             'chat_id': self.chat_id,
    #             'text': text
    #         }
    #     )
