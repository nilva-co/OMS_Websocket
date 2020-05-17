from time import sleep

from models import *
from webservices import Hub

if __name__ == "__main__":
    url = 'https://boursei.ephoenix.ir/realtime'
    user = 'samin'
    password = '123456789'
    hub = Hub(url)
    hub.login(user, password)
    # hub.connect()