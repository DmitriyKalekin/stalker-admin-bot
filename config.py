import os
from __private__.telegram_key import CFG_TELEGRAM_KEY


class Config:
    ENV = os.getenv('ENV')
    PORT = 8443
    REUSE_PORT = True
    TELEGRAM_KEY = CFG_TELEGRAM_KEY
    URL = f'https://api.telegram.org/bot{TELEGRAM_KEY}/'
    DEBUG = True    
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASS = "123123"
    MYSQL_DBNM = "stalker"
    

class LocalConfig(Config):
    HOST = "127.0.0.1"
    PORT = 5000
    REUSE_PORT = False
    WH_URL = f'https://eva-bot.ru:{PORT}/run_wh'
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASS = "123123"
    MYSQL_DBNM = "stalker"


class MasterConfig(Config):
    HOST = "0.0.0.0"
    PORT = 8443
    REUSE_PORT = True
    WH_URL = f'https://eva-bot.ru:{PORT}/run_wh'
    MYSQL_HOST = "178.128.199.55"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASS = "123123"
    MYSQL_DBNM = "stalker"


def get_config():
    print("ENV =====", os.getenv('ENV'))
    if os.getenv('ENV') == "Local":
        return LocalConfig()

    if os.getenv('ENV') == "Master":
        return MasterConfig()

    return MasterConfig()
     
