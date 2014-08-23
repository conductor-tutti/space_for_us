class Config(object):
    SECRET_KEY = "you_will_never_know_this_key"
    FACEBOOK_APP_ID = "944323692250762"
    FACEBOOK_APP_SECRET = "207996ac76593a7fe2dd9930ecb79ce5"
    debug = False

class Production(Config):
    debug = True
