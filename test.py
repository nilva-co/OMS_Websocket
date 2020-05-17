from models import *
from webservices import Hub

if __name__ == "__main__":
    # url = 'http://localhost:5000/chatHub'
    url = 'https://boursei.ephoenix.ir/realtime'
    user = 'samin'
    password = '123456789'
    hub = Hub(url, user, password)
    hub.login(user, password, url)
