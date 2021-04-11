import os
import hmac
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
        
        headers = {
            'CB-ACCESS-KEY': os.getenv('CB_KEY'),
            'CB-ACCESS-SIGN': hmac(os.getenv('CB_SECRET'), '{}{}{}'.format(str(result['data']['epoch']), 'GET', '/accounts')),
            'CB-ACCESS-TIMESTAMP': str(result['data']['epoch'])
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