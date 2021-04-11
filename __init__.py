import json, hmac, hashlib, time, os, requests
from requests.auth import AuthBase
from mycroft import MycroftSkill, intent_handler

API_KEY = os.getenv('CB_KEY', '')
API_SECRET = os.getenv('CB_SECRET', '')

class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request

class CryptoSkill(MycroftSkill):
    def __init__(self):
        super(CryptoSkill, self).__init__("CryptoSkill")
        self.log.info(API_KEY, API_SECRET)
        self.auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

    @intent_handler('what.is.my.crypto.balance.intent')
    def get_crypto_balance(self):
        
        r = requests.get('https://api.coinbase.com/v2/accounts', auth=self.auth)
        self.log.warn(r.json())
        
        # use some sort of imported service to make request to coinbase API
        balance = '19999.05'
        # parse returned data

        # publish on topic for frontend use
        self.log.info('we have %s in our account', balance)


def create_skill():
    return CryptoSkill()