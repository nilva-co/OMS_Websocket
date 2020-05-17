import time

from gevent import monkey as curious_george

from logic import main

curious_george.patch_all(thread=False, select=False)
from requests import Session
from signalr import Connection


class Hub:
    token = None
    # token = 'AQAAANCMnd8BFdERjHoAwE_Cl-sBAAAAeszMjFsAq02WR2mA7Cux3wAAAAACAAAAAAAQZgAAAAEAACAAAAAU5qRWjn6CbVOyZRfI8GQDTFgp2oCT5oh7rg8cadCb0gAAAAAOgAAAAAIAACAAAABqsTfLNXTE43Wgz8zQHGJrhM3E1Cs9nroSmGTvZWuJrFAAAAAaeVfaCwZ5n1ktBvvFRpAMbzDR9a-YQOv1rFgUUnNpO3BQqVZb3IwHfKyh5a8siJ9yp63GSpUDCbhNI5eVEcAP91mLPozgWycKoW-djv9CUUAAAAC_qzXONjCXmJJjdIx95Wht3ih5Txe3Sjxgz0MH6M4m171BVN2rBwzCuvAaRhBlprMmkG9S2F_ladcnG16O7htt'
    hub_connection = None
    connection = None
    hub = None
    token_hub = None

    def __init__(self, url, log=False):
        self.url = url
        self.log = log

    def token_get(self, **data):
        if 'R' in data:
            print('token:\n', data['R'])
        if 'R' in data:
            if 'ex' in data['R']:
                return
            self.token = data['R']
            self.connection.received -= self.token_get
            self.connection.close()
            self.connect()

    def stop(self):
        self.connection.close()
        self.hub_connection.close()

    def connect(self):
        # with Session() as session:
        with Session() as session:
            # create a connection

            self.hub_connection = Connection(self.url, session, self.token)

            def print_error(error):
                print('error: ', error)

            def default_received(**data):
                if self.log:
                    print("msg log:\n", data)

                if 'R' in data:
                    if 'ex' in data['R']:
                        self.error_handler(data['R']['ex'])

            self.hub_connection.error += print_error
            self.hub_connection.received += default_received

            self.hub = self.hub_connection.register_hub('OmsClientHub')

            self.hub.client.on("orderAdded", self.OrderAdded)
            self.hub.client.on("orderEdited", self.OrderEdited)
            self.hub.client.on("orderStateChange", self.OrderStateChange)
            self.hub.client.on("orderExecution", self.OrderExecution)
            self.hub.client.on("orderError", self.OrderError)
            self.hub.client.on("showError", self.ShowError)
            self.hub.client.on("creditInfoUpdate", self.CreditInfoUpdate)
            self.hub.client.on("assetPriceChange", self.AssetPriceChange)
            self.hub.client.on("assetChange", self.AssetChange)
            self.hub.client.on("positionChange", self.PositionChange)
            self.hub.client.on("removeAsset", self.RemoveAsset)
            self.hub.client.on("activeInstrumentBestLimitChange", self.ActiveInstrumentBestLimitChange)
            self.hub.client.on("activeInstrumentThresholdsChange", self.ActiveInstrumentThresholdsChange)
            self.hub.client.on("instrumentFirstBestLimitChange", self.InstrumentFirstBestLimitChange)
            self.hub.client.on("instrumentTrade", self.InstrumentTrade)
            self.hub.client.on("instrumentStateChange", self.InstrumentStateChange)
            self.hub.client.on("instrumentTradePercentChage", self.InstrumentTradePercentChage)
            self.hub.client.on("instrumentClosingPriceChange", self.InstrumentClosingPriceChange)
            self.hub.client.on("instrumentEPSDataChange", self.InstrumentEPSDataChange)
            self.hub.client.on("overallStatisticsChange", self.OverallStatisticsChange)
            self.hub.client.on("initUI", self.InitUI)
            self.hub.client.on("instrumentAdded", self.InstrumentAdded)
            self.hub.client.on("instrumentRemoved", self.InstrumentRemoved)

            with self.hub_connection:
                main(self)
                self.hub_connection.wait(100)

    def login(self, userId, password):
        with Session() as session:
            # create a connection
            self.connection = Connection(self.url, session)
            self.token_hub = self.connection.register_hub('OmsClientTokenHub')

            def print_error(error):
                print('error: ', error)

            def default_received(**data):
                if self.log:
                    print("msg log:\n", data)

            self.connection.error += print_error
            self.connection.received += default_received

            with self.connection:
                self._login(userId, password)

                self.connection.wait(1)

    def error_handler(self, *args, **kwargs):
        print('error:\n', *args)
        # implement your error handler here

    ### server ###
    def _login(self, *data):
        self.connection.received += self.token_get
        self.token_hub.server.invoke('GetNewAPIToken', *data)

    def AddOrder(self, *args, **kwargs):
        self.hub.server.invoke("AddOrder", *args, **kwargs)

    def EditOrder(self, *args, **kwargs):
        self.hub.server.invoke("EditOrder", *args)

    def CancelOrder(self, *args, **kwargs):
        self.hub.server.invoke("CancelOrder", *args)

    def GetTime(self, *args, **kwargs):
        self.hub.server.invoke("GetTime", *args)

    def Logout(self, *args, **kwargs):
        self.hub.server.invoke("Logout")

    def AddInstrumentToMarketwatch(self, *args, **kwargs):
        self.hub.server.invoke("AddInstrumentToMarketwatch", *args)

    def RemoveInstrumentFromMarketwatch(self, *args, **kwargs):
        self.hub.server.invoke("RemoveInstrumentFromMarketwatch", *args)

    def SetActiveInstrument(self, *args, **kwargs):
        self.hub.server.invoke("SetActiveInstrument", *args)

    def GetInstrumentList(self, *args, **kwargs):
        self.hub.server.invoke("GetInstrumentList")

    def ChangeMarketWatch(self, *args, **kwargs):
        self.hub.server.invoke("ChangeMarketWatch", *args)

    def AddNewMarketWatch(self, *args, **kwargs):
        self.hub.server.invoke("AddNewMarketWatch", *args)

    def RemoveMarketwatch(self, *args, **kwargs):
        self.hub.server.invoke("RemoveMarketwatch", *args)

    def GetAcountRemainReport(self, *args, **kwargs):
        self.hub.server.invoke("GetAcountRemainReport", *args)

    def GetOrderListReport(self, *args, **kwargs):
        self.hub.server.invoke("GetOrderListReport", args)

    def GetInstrumentDetailForOrder(self, *args, **kwargs):
        self.hub.server.invoke("GetInstrumentDetailForOrder", *args)

    ### Client ###
    def OrderAdded(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def OrderEdited(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def OrderStateChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def OrderExecution(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def OrderError(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def ShowError(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def CreditInfoUpdate(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def AssetPriceChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def AssetChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def PositionChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def RemoveAsset(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def ActiveInstrumentBestLimitChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def ActiveInstrumentThresholdsChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentFirstBestLimitChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentTrade(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentStateChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentTradePercentChage(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentClosingPriceChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentEPSDataChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def OverallStatisticsChange(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InitUI(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentAdded(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here

    def InstrumentRemoved(self, *args, **kwargs):
        print("args: \n", args)
        # implement your code here
