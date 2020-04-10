from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder
from base64 import b64decode
from zlib import decompress, MAX_WBITS

from signalr import Connection

from APIModels import *
from models import ObjectEncoder


def process_message(message):
    deflated_msg = decompress(b64decode(message), -MAX_WBITS)
    return json.loads(deflated_msg.decode())


class Hub:
    token = None
    hub_connection = None

    def __init__(self, server_url, userId, password):
        self.server_url = server_url
        # self.login(userId, password)

    def setToken(self, data):
        self.token = process_message(data)['token']

    def login(self, userId, password, login_url=None):
        with requests.Session() as session:
            if login_url:
                connection = Connection(login_url, session)
            else:
                connection = Connection(self.server_url, session)
            apiTokenHub = connection.register_hub('GetNewAPIToken')
            connection.start()
            apiTokenHub.client.on('GetAPIToken', self.setToken)

            credentials = json.dumps({"userId": userId, "password": password}, cls=ObjectEncoder)
            with connection:
                apiTokenHub.server.invoke('GetAPIToken', credentials)
            # connection.close()

        # response = requests.post(self.server_url, data={"userId": userId, "password": password})
        # self.token = response.json()["token"]
        # return self.token

    def connect(self):
        self.hub_connection = HubConnectionBuilder() \
            .with_url(self.server_url, options={
            "token": self.token
        }).with_automatic_reconnect({
            "type": "interval",
            "keep_alive_interval": 10,
            "intervals": [1, 3, 5, 6, 7, 87, 3]
        }) \
            .build()

        self.hub_connection.on("OrderAdded", self.OrderAdded)
        self.hub_connection.on("OrderEdited", self.OrderEdited)
        self.hub_connection.on("OrderStateChange", self.OrderStateChange)
        self.hub_connection.on("OrderExecution", self.OrderExecution)
        self.hub_connection.on("OrderError", self.OrderError)
        self.hub_connection.on("ShowError", self.ShowError)
        self.hub_connection.on("CreditInfoUpdate", self.CreditInfoUpdate)
        self.hub_connection.on("AssetPriceChange", self.AssetPriceChange)
        self.hub_connection.on("AssetChange", self.AssetChange)
        self.hub_connection.on("PositionChange", self.PositionChange)
        self.hub_connection.on("RemoveAsset", self.RemoveAsset)
        self.hub_connection.on("ActiveInstrumentBestLimitChange", self.ActiveInstrumentBestLimitChange)
        self.hub_connection.on("ActiveInstrumentThresholdsChange", self.ActiveInstrumentThresholdsChange)
        self.hub_connection.on("InstrumentFirstBestLimitChange", self.InstrumentFirstBestLimitChange)
        self.hub_connection.on("InstrumentTrade", self.InstrumentTrade)
        self.hub_connection.on("InstrumentStateChange", self.InstrumentStateChange)
        self.hub_connection.on("InstrumentTradePercentChage", self.InstrumentTradePercentChage)
        self.hub_connection.on("InstrumentClosingPriceChange", self.InstrumentClosingPriceChange)
        self.hub_connection.on("InstrumentEPSDataChange", self.InstrumentEPSDataChange)
        self.hub_connection.on("OverallStatisticsChange", self.OverallStatisticsChange)
        self.hub_connection.on("InitUI", self.InitUI)
        self.hub_connection.on("InstrumentAdded", self.InstrumentAdded)
        self.hub_connection.on("InstrumentRemoved", self.InstrumentRemoved)

        self.hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.start()

    def stop(self):
        self.hub_connection.stop()

    ### server ###

    def AddOrder(self, data: AddOrder):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("AddOrder", msg)

    def EditOrder(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("EditOrder", msg)

    def CancelOrder(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("CancelOrder", msg)

    def GetTime(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("GetTime", msg)

    def Logout(self, data=None):
        self.hub_connection.send("Logout")

    def AddInstrumentToMarketwatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("AddInstrumentToMarketwatch", msg)

    def RemoveInstrumentFromMarketwatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("RemoveInstrumentFromMarketwatch", msg)

    def SetActiveInstrument(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("SetActiveInstrument", msg)

    def GetInstrumentList(self, data=None):
        self.hub_connection.send("GetInstrumentList")

    def ChangeMarketWatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("ChangeMarketWatch", msg)

    def AddNewMarketWatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("AddNewMarketWatch", msg)

    def RemoveMarketwatch(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("RemoveMarketwatch", msg)

    def GetAcountRemainReport(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("GetAcountRemainReport", msg)

    def GetOrderListReport(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("GetOrderListReport", msg)

    def GetInstrumentDetailForOrder(self, data):
        msg = json.dumps(data, cls=ObjectEncoder)
        self.hub_connection.send("GetInstrumentDetailForOrder", msg)

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
