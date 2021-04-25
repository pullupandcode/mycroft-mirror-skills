import json, hmac, hashlib, time, os, requests
from requests.auth import AuthBase
from mycroft import MycroftSkill, intent_handler
import redis

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
            'CB-VERSION': '2021-01-01'
        })
        return request


class CryptoSkill(MycroftSkill):
    # remember to add pub channels via env variables
    # pull out redis host info into env variables
    def __init__(self):
        super(CryptoSkill, self).__init__("CryptoSkill")
        self.auth = CoinbaseWalletAuth(API_KEY, API_SECRET)
        self.redis_client = redis.Redis(host="192.168.1.11", port=6379, db=0)

    @intent_handler('what.is.my.crypto.balance.intent')
    def get_crypto_balance(self):
        r = requests.get('https://api.coinbase.com/v2/accounts', auth=self.auth)
        result = r.json()

        response_message = self.parse_cb_response(result.get("data"))

        self.redis_client.publish('crypto_balance', json.dumps(response_message), separators=(',', ':'))
        self.log.info('==== message published ====')
    
    def parse_cb_response(data):
        currency_list = []
        usd_currency_value_list = []
        usd_prices = []

        parsed_data = json.loads(data)
        for account in parsed_data:
            currency_list.append({"curr": account.get('balance').get('currency'), "val": account.get('balance').get('amount')})

        for account in currency_list:
            response = requests.get("https://api.coinbase.com/v2/exchange-rates", {"currency": account.get('curr')}).json()
            usd_value = response.get("data").get("rates").get("USD")
            usd_prices.append(float(usd_value) * float(account.get("val")))

            usd_currency_value_list.append({"currency": account.get("curr"), "usd_value": '%.2f' % (float( usd_value) * float(account.get("val")))})

        usd_currency_value_list.append({"total": reduce(lambda x, y: x + y, usd_prices)})
        return usd_currency_value_list

def create_skill():
    return CryptoSkill()