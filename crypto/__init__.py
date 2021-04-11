from mycroft import MycroftSkill, intent_handler

class CryptoSkill(MycroftSkill):
    def __init__(self):
        super.__init__()

    @intent_handler('what.is.my.crypto.balance')
    def get_crypto_balance(self):
        # use some sort of imported service to make request to coinbase API
        balance = '19999.05'
        # parse returned data

        # publish on topic for frontend use
        self.log.info('we have %s in our account', balance)


def create_skill():
    return CryptoSkill()