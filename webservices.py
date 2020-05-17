import time

from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)
from requests import Session
from signalr import Connection

from base64 import b64decode
from zlib import decompress, MAX_WBITS

# from signalr import Connection

from APIModels import *
from models import ObjectEncoder


def process_message(message):
    deflated_msg = decompress(b64decode(message), -MAX_WBITS)
    return json.loads(deflated_msg.decode())


class Hub:
    token = None
    hub_connection = None
    connection = None
    hub = None
    token_hub = None
    url = 'https://boursei.ephoenix.ir/realtime'

    def setToken(self, data):
        self.token = process_message(data)['token']

    def login(self, userId, password):
        with Session() as session:
            # create a connection
            self.connection = Connection(self.url, session)
            self.token_hub = self.connection.register_hub('OmsClientTokenHub')

            def print_error(error):
                print('error: ', error)

            def default_received(**data):
                print("default msg receive:\n", data)

            self.connection.error += print_error
            self.connection.received += default_received

            self.connection.start()
            self.Login(userId, password)

    def message(self, **first):
        print(first)

    def connect(self):
        # with Session() as session:
        session = Session()
        # create a connection
        session.headers.update({'token': '{tok}'.format(tok=self.token)})
        self.hub_connection = Connection(self.url, session)

        def print_error(error):
            print('error: ', error)

        def default_received(**data):
            print("default msg receive:\n", data)

            if "'ex'" in data:
                print_error(data['R'])

        self.hub_connection.error += print_error
        self.hub_connection.received += default_received

        self.hub = self.hub_connection.register_hub('OmsClientHub')

        self.hub.on("OrderAdded", self.OrderAdded)
        self.hub.on("OrderEdited", self.OrderEdited)
        self.hub.on("OrderStateChange", self.OrderStateChange)
        self.hub.on("OrderExecution", self.OrderExecution)
        self.hub.on("OrderError", self.OrderError)
        self.hub.on("ShowError", self.ShowError)
        self.hub.on("CreditInfoUpdate", self.CreditInfoUpdate)
        self.hub.on("AssetPriceChange", self.AssetPriceChange)
        self.hub.on("AssetChange", self.AssetChange)
        self.hub.on("PositionChange", self.PositionChange)
        self.hub.on("RemoveAsset", self.RemoveAsset)
        self.hub.on("ActiveInstrumentBestLimitChange", self.ActiveInstrumentBestLimitChange)
        self.hub.on("ActiveInstrumentThresholdsChange", self.ActiveInstrumentThresholdsChange)
        self.hub.on("InstrumentFirstBestLimitChange", self.InstrumentFirstBestLimitChange)
        self.hub.on("InstrumentTrade", self.InstrumentTrade)
        self.hub.on("InstrumentStateChange", self.InstrumentStateChange)
        self.hub.on("InstrumentTradePercentChage", self.InstrumentTradePercentChage)
        self.hub.on("InstrumentClosingPriceChange", self.InstrumentClosingPriceChange)
        self.hub.on("InstrumentEPSDataChange", self.InstrumentEPSDataChange)
        self.hub.on("OverallStatisticsChange", self.OverallStatisticsChange)
        self.hub.on("InitUI", self.InitUI)
        self.hub.on("InstrumentAdded", self.InstrumentAdded)
        self.hub.on("InstrumentRemoved", self.InstrumentRemoved)

        # self.hub.on_open(lambda: print("connection opened and handshake received ready to send messages"))
        # self.hub.on_close(lambda: print("connection closed"))
        self.hub.start()

    def stop(self):
        self.hub_connection.close()

    ### server ###

    def Login(self, *data):
        def token_get(**data):
            print('token:\n', data)
            if "'R'" in data:
                self.token = data['R']
                self.connection.received -= token_get
                self.connection.close()
                self.connect()

        self.connection.received += token_get
        self.token_hub.server.invoke('GetNewAPIToken', *data)

    def AddOrder(self, *data):
        # msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("AddOrder", *data)

    def EditOrder(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("EditOrder", msg)

    def CancelOrder(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("CancelOrder", msg)

    def GetTime(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("GetTime", msg)

    def Logout(self, data=None):
        self.hub.server.invoke("Logout")

    def AddInstrumentToMarketwatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("AddInstrumentToMarketwatch", msg)

    def RemoveInstrumentFromMarketwatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("RemoveInstrumentFromMarketwatch", msg)

    def SetActiveInstrument(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("SetActiveInstrument", msg)

    def GetInstrumentList(self, data=None):
        self.hub.server.invoke("GetInstrumentList")

    def ChangeMarketWatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("ChangeMarketWatch", msg)

    def AddNewMarketWatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("AddNewMarketWatch", msg)

    def RemoveMarketwatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("RemoveMarketwatch", msg)

    def GetAcountRemainReport(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("GetAcountRemainReport", msg)

    def GetOrderListReport(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("GetOrderListReport", msg)

    def GetInstrumentDetailForOrder(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub.server.invoke("GetInstrumentDetailForOrder", msg)

    ### Client ###

    def OrderAdded(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return OrderAdded.from_json(msg)

    def OrderEdited(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return OrderEdited.from_json(msg)

    def OrderStateChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return OrderStateChange.from_json(msg)

    def OrderExecution(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return OrderExecution.from_json(msg)

    def OrderError(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return OrderError.from_json(msg)

    def ShowError(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return ShowError.from_json(msg)

    def CreditInfoUpdate(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return CreditInfoUpdate.from_json(msg)

    def AssetPriceChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return AssetPriceChange.from_json(msg)

    def AssetChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return AssetChange.from_json(msg)

    def PositionChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return PositionChange.from_json(msg)

    def RemoveAsset(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return RemoveAsset.from_json(msg)

    def ActiveInstrumentBestLimitChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return ActiveInstrumentBestLimitChange.from_json(msg)

    def ActiveInstrumentThresholdsChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return ActiveInstrumentThresholdsChange.from_json(msg)

    def InstrumentFirstBestLimitChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentFirstBestLimitChange.from_json(msg)

    def InstrumentTrade(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentTrade.from_json(msg)

    def InstrumentStateChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentStateChange.from_json(msg)

    def InstrumentTradePercentChage(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentTradePercentChage.from_json(msg)

    def InstrumentClosingPriceChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentClosingPriceChange.from_json(msg)

    def InstrumentEPSDataChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentEPSDataChange.from_json(msg)

    def OverallStatisticsChange(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return OverallStatisticsChange.from_json(msg)

    def InitUI(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InitUI.from_json(msg)

    def InstrumentAdded(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentAdded.from_json(msg)

    def InstrumentRemoved(self, data):
        msg = process_message(data)
        if msg['ex']:
            pass
        return InstrumentRemoved.from_json(msg)
