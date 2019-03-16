from main import api
from settings import SETTINGS
from urls import *

if __name__ == '__main__':
    api.secret_key = 'hoge'
    api.run(host=SETTINGS['FLASK_URL'], port=SETTINGS['FLASK_PORT'])
