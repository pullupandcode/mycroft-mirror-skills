from mycroft import MycroftSkill, intent_handler
import CoinbaseWalletAuth
import requests

API_KEY = os.getenv('CB_KEY')
API_SECRET = os.getenv('CB_SECRET')

class CryptoSkill(MycroftSkill):
    def __init__(self):
        super(CryptoSkill, self).__init__("CryptoSkill")
        self.request_auth = new CoinbaseWalletAuth(API_KEY, API_SECRET)

    @intent_handler('what.is.my.crypto.balance.intent')
    def get_crypto_balance(self):
        
        r = requests.get('https://api.coinbase.com/v2/accounts', auth=self.request_auth)
        self.log.warn(r.json())
        
        # use some sort of imported service to make request to coinbase API
        balance = '19999.05'
        # parse returned data

        # publish on topic for frontend use
        self.log.info('we have %s in our account', balance)


def create_skill():
    return CryptoSkill()