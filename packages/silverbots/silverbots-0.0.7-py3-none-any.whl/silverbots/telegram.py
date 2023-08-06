import requests


class Telegram:
    def __init__(self, token):
        self.token = token

    def send_message(self, chat, text):
        web = f"https://api.telegram.org/bot{self.token}/sendMessage"
        msg = {
            "chat_id": chat,
            "text": text
        }
        requests.post(web, json=msg)
