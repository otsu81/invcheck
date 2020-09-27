import logging
import json
import os
import http.client


CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_API_HOST = 'api.telegram.org'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('telegram broadcaster')


class Telegram():

    def __init__(self):
        pass

    def send(self, message):
        log.info(message)

        if TELEGRAM_TOKEN is not None:
            connection = http.client.HTTPSConnection(TELEGRAM_API_HOST)
            endpoint = f"/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {
                'chat_id': CHAT_ID,
                'text': message
            }
            headers = {'content-type': "application/json"}

            connection.request(
                'POST', endpoint, json.dumps(payload), headers
            )
            result = connection.getresponse()

            if result.status != '200':
                log.warn(f"Response status from telegram: {result.status}")

            return {
                'message': message,
                'response': result.status
            }
        else:
            log.warn('No telegram token specified')