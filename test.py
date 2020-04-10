from models import *
from webservices import Hub

if __name__ == "__main__":
    data = StateChangeData(10, OrderStatus.Canceled, 23, "ahmad", OrderLockType.LockForCancel, 12, 123,
                           OrderSource.Admin)
    string = json.dumps(data, cls=ObjectEncoder)
    print(string)
    print(data)
    x = StateChangeData.from_json(json.loads(string))
    print(x.OrderSource)

    url = 'wss://boursei.exphoenixtrade.com/realtime'
    user = 'samin'
    password = '123456789'
    hub = Hub(url, user, password)
    hub.login(user, password, url)
