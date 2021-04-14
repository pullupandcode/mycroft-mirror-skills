import os
import hmac
import hashlib
import time
from mycroft import MycroftSkill, intent_handler
import requests

class CryptoSkill(MycroftSkill):
    def __init__(self):
        super(CryptoSkill, self).__init__("CryptoSkill")

    @intent_handler('what.is.my.crypto.balance.intent')
    def get_crypto_balance(self):
        time_request = requests.get('https://api.coinbase.com/v2/time')
        result = time_request.json()
        self.log.info(result)
        apikey = os.getenv('CB_SECRET', '')
        signed_payload = hmac.new(
            key=apikey.encode('utf-8'), 
            msg=f"{str(result['data']['epoch'])}GET/v2/accounts".encode('utf-8'), 
            digestmod=hashlib.sha256
            ).hexdigest()

        headers = {
            'CB-ACCESS-KEY': os.getenv('CB_KEY'),
            'CB-ACCESS-SIGN': signed_payload,
            'CB-ACCESS-TIMESTAMP': f"{str(result['data']['epoch'])}",
            'CB-VERSION': '2021-01-01'
        }
        r = requests.get('https://api.coinbase.com/v2/accounts', headers=headers)
        self.log.warn(r.json())
        
        # use some sort of imported service to make request to coinbase API
        balance = '19999.05'
        # parse returned data

        # publish on topic for frontend use
        self.log.info('we have %s in our account', balance)


def create_skill():
    return CryptoSkill()