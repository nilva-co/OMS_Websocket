from models import *
from webservices import Hub

if __name__ == "__main__":
    # url = 'http://localhost:5000/chatHub'
    user = 'samin'
    password = '123456789'
    hub = Hub()
    hub.login(user, password)
