from models import *


class AddOrder:
    def __init__(self, OrderSide,
                 InstrumentId,
                 Quantity,
                 Price,
                 CreditSource,
                 MinimumQuantity,
                 DisclosedQuantity,
                 Validity,
                 ValidityDateYear,
                 ValidityDateMonth,
                 ValidityDateDay,
                 Repeat,
                 ExtraData
                 ):
        self.OrderSide = OrderSide
        self.InstrumentId = InstrumentId
        self.Quantity = Quantity
        self.Price = Price
        self.CreditSource = CreditSource
        self.MinimumQuantity = MinimumQuantity
        self.DisclosedQuantity = DisclosedQuantity
        self.Validity = Validity
        self.ValidityDateYear = ValidityDateYear
        self.ValidityDateMonth = ValidityDateMonth
        self.ValidityDateDay = ValidityDateDay
        self.Repeat = Repeat
        self.ExtraData = ExtraData

    def to_json(self):
        return {"OrderSide": self.OrderSide,
                "InstrumentId": self.InstrumentId,
                "Quantity": self.Quantity,
                "Price": self.Price,
                "CreditSource": self.CreditSource,
                "MinimumQuantity": self.MinimumQuantity,
                "DisclosedQuantity": self.DisclosedQuantity,
                "Validity": self.Validity,
                "ValidityDate.Year": self.ValidityDateYear,
                "ValidityDate.Month": self.ValidityDateMonth,
                "ValidityDate.Day": self.ValidityDateDay,
                "Repeat": self.Repeat,
                "ExtraData": self.ExtraData}


class EditOrder:
    def __init__(self, Id,
                 Quantity,
                 Price,
                 MinimumQuantity,
                 DisclosedQuantity,
                 Validity,
                 ValidityDateYear,
                 ValidityDateMonth,
                 ValidityDateDay
                 ):
        self.Id = Id
        self.Quantity = Quantity
        self.Price = Price
        self.MinimumQuantity = MinimumQuantity
        self.DisclosedQuantity = DisclosedQuantity
        self.Validity = Validity
        self.ValidityDateYear = ValidityDateYear
        self.ValidityDateMonth = ValidityDateMonth
        self.ValidityDateDay = ValidityDateDay

    def to_json(self):
        return {"Id": self.Id,
                "Quantity": self.Quantity,
                "Price": self.Price,
                "MinimumQuantity": self.MinimumQuantity,
                "DisclosedQuantity": self.DisclosedQuantity,
                "Validity": self.Validity,
                "ValidityDate.Year": self.ValidityDateYear,
                "ValidityDate.Month": self.ValidityDateMonth,
                "ValidityDate.Day": self.ValidityDateDay,
                }


class CancelOrder:
    def __init__(self, Id):
        self.Id = Id


class GetTime:
    def __init__(self, Time):
        self.Time = Time


class AddInstrumentToMarketwatch:
    def __init__(self, instrumentId):
        self.instrumentId = instrumentId


class RemoveInstrumentToMarketwatch:
    def __init__(self, instrumentId):
        self.instrumentId = instrumentId


class SetActiveInstrument:
    def __init__(self, instrumentId):
        self.instrumentId = instrumentId


class ChangeMarketWatch:
    def __init__(self, Id):
        self.Id = Id


class AddNewMarketWatch:
    def __init__(self, Name):
        self.Name = Name


class RemoveMarketwatch:
    def __init__(self, Id):
        self.Id = Id


class GetAcountRemainReport:
    def __init__(self, ReportType,
                 FromYear,
                 FromMonth,
                 FromDay,
                 ToYear,
                 ToMonth,
                 ToDay
                 ):
        self.ReportType = ReportType
        self.FromYear = FromYear
        self.FromMonth = FromMonth
        self.FromDay = FromDay
        self.ToYear = ToYear
        self.ToMonth = ToMonth
        self.ToDay = ToDay


class GetOrderListReport:
    def __init__(self, instrumentId,
                 orderStatus,
                 FromYear,
                 FromMonth,
                 FromDay,
                 ToYear,
                 ToMonth,
                 ToDay
                 ):
        self.instrumentId = instrumentId
        self.orderStatus = orderStatus
        self.FromYear = FromYear
        self.FromMonth = FromMonth
        self.FromDay = FromDay
        self.ToYear = ToYear
        self.ToMonth = ToMonth
        self.ToDay = ToDay


class GetInstrumentDetailForOrder:
    def __init__(self, instrumentId):
        self.instrumentId = instrumentId


class OrderAdded:
    def __init__(self, OrderData):
        self.OrderData = OrderData

    @classmethod
    def from_json(cls, data: dict):
        return cls(OrderData=OrderData.from_json(data.pop("OrderData")))


class OrderEdited:
    def __init__(self, StateChangeData,
                 Quantity,
                 Price,
                 ExecutedQuantity,
                 Validity,
                 OrderValidityDate,
                 DisclosedQuantity,
                 MinimumQuantity,
                 Remain
                 ):
        self.StateChangeData = StateChangeData
        self.Quantity = Quantity
        self.Price = Price
        self.ExecutedQuantity = ExecutedQuantity
        self.Validity = Validity
        self.OrderValidityDate = OrderValidityDate
        self.DisclosedQuantity = DisclosedQuantity
        self.MinimumQuantity = MinimumQuantity
        self.Remain = Remain

    @classmethod
    def from_json(cls, data: dict):
        return cls(StateChangeData=StateChangeData.from_json(data.pop("StateChangeData")),
                   Validity=OrderValidity(data.pop("Validity")),
                   OrderValidityDate=Date.from_json(data.pop("OrderValidityDate")), **data)


class OrderStateChange:
    def __init__(self, StateChangeData):
        self.StateChangeData = StateChangeData

    @classmethod
    def from_json(cls, data: dict):
        return cls(StateChangeData=StateChangeData.from_json(data.pop("StateChangeData")))


class OrderExecution:
    def __init__(self, Id,
                 ExecutedQuantity,
                 OrderStatus,
                 OrderLockType,
                 BlockedCredit,
                 Remain,
                 Quantity,
                 Price,
                 DraftAmount
                 ):
        self.Id = Id
        self.ExecutedQuantity = ExecutedQuantity
        self.OrderStatus = OrderStatus
        self.OrderLockType = OrderLockType
        self.BlockedCredit = BlockedCredit
        self.Remain = Remain
        self.Quantity = Quantity
        self.Price = Price
        self.DraftAmount = DraftAmount

    @classmethod
    def from_json(cls, data: dict):
        return cls(OrderStatus=OrderStatus(data.pop("OrderStatus")),
                   OrderLockType=OrderLockType(data.pop("OrderLockType")),
                   **data)


class OrderError:
    def __init__(self, StateChangeData, ErrorMessage):
        self.StateChangeData = StateChangeData
        self.ErrorMessage = ErrorMessage

    @classmethod
    def from_json(cls, data: dict):
        return cls(StateChangeData=StateChangeData.from_json(data.pop("StateChangeData")), **data)


class ShowError:
    def __init__(self, Error):
        self.Error = Error

    @classmethod
    def from_json(cls, data: dict):
        return cls(Error=ErrorObject.from_json(data['Error']))


class CreditInfoUpdate:
    def __init__(self, AccountInfo):
        self.AccountInfo = AccountInfo

    @classmethod
    def from_json(cls, data: dict):
        return cls(AccountInfo=AccountInfo.from_json(data['AccountInfo']))


class AssetPriceChange:
    def __init__(self, Id,
                 LastTradePrice
                 ):
        self.Id = Id
        self.LastTradePrice = LastTradePrice

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class AssetChange:
    def __init__(self, AssetData):
        self.AssetData = AssetData

    @classmethod
    def from_json(cls, data: dict):
        return cls(AssetData=AssetData.from_json(data['AssetData']))


class PositionChange:
    def __init__(self, PositionData):
        self.PositionData = PositionData

    @classmethod
    def from_json(cls, data: dict):
        return cls(PositionData=PositionDataArray.from_json(data['PositionData']))


class RemoveAsset:
    def __init__(self, Id):
        self.Id = Id

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class ActiveInstrumentBestLimitChange:
    def __init__(self, Id,
                 BestLimit
                 ):
        self.Id = Id
        self.BestLimit = BestLimit

    @classmethod
    def from_json(cls, data: dict):
        return cls(BestLimit=BestLimitData.from_json(data['BestLimit']), **data)


class ActiveInstrumentThresholdsChange:
    def __init__(self, Id,
                 ThresholdHigh,
                 ThresholdLow
                 ):
        self.Id = Id
        self.ThresholdHigh = ThresholdHigh
        self.ThresholdLow = ThresholdLow

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class InstrumentFirstBestLimitChange:
    def __init__(self, Id,
                 BestLimit
                 ):
        self.Id = Id
        self.BestLimit = BestLimit

    @classmethod
    def from_json(cls, data: dict):
        return cls(BestLimit=BestLimitData.from_json(data['BestLimit']), **data)


class InstrumentTrade:
    def __init__(self, Id,
                 HighestPrice,
                 LowestPrice,
                 FirstPrice,
                 LastTradePrice,
                 LastTradeDate,
                 NumberOfTrades,
                 MarketQuanity
                 ):
        self.Id = Id
        self.HighestPrice = HighestPrice
        self.LowestPrice = LowestPrice
        self.FirstPrice = FirstPrice
        self.LastTradePrice = LastTradePrice
        self.LastTradeDate = LastTradeDate
        self.NumberOfTrades = NumberOfTrades
        self.MarketQuanity = MarketQuanity

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class InstrumentStateChange:
    def __init__(self, Id,
                 StateId,
                 NscStateId
                 ):
        self.Id = Id
        self.StateId = StateId
        self.NscStateId = NscStateId

    @classmethod
    def from_json(cls, data: dict):
        return cls(NscStateId=NscState(data.pop("NscStateId")), **data)


class InstrumentTradePercentChage:
    def __init__(self, Id,
                 NumberOfTrades,
                 TradePercentChageData
                 ):
        self.Id = Id
        self.NumberOfTrades = NumberOfTrades
        self.TradePercentChageData = TradePercentChageData

    @classmethod
    def from_json(cls, data: dict):
        return cls(TradePercentChageData=TradePercentChange.from_json(data['TradePercentChageData']), **data)


class InstrumentClosingPriceChange:
    def __init__(self, Id,
                 NumberOfTrades,
                 MarketQuanity,
                 SectorPE,
                 FinalPrice,
                 YesterdayFinalPrice,
                 YesterdayLastTradePrice,
                 NoData
                 ):
        self.Id = Id
        self.NumberOfTrades = NumberOfTrades
        self.MarketQuanity = MarketQuanity
        self.SectorPE = SectorPE
        self.FinalPrice = FinalPrice
        self.YesterdayFinalPrice = YesterdayFinalPrice
        self.YesterdayLastTradePrice = YesterdayLastTradePrice
        self.NoData = NoData

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class InstrumentEPSDataChange:
    def __init__(self, Id,
                 EstimatedEPS,
                 SectorPE
                 ):
        self.Id = Id
        self.EstimatedEPS = EstimatedEPS
        self.SectorPE = SectorPE

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class OverallStatisticsChange:
    def __init__(self, MarketOverallStatistics):
        self.MarketOverallStatistics = MarketOverallStatistics

    @classmethod
    def from_json(cls, data: dict):
        return cls(MarketOverallStatistics=MarketOverallStatistics.from_json(data["MarketOverallStatistics"]))


class InitUI:
    def __init__(self, AppData,
                 InvestorData,
                 MarketWatchItems
                 ):
        self.AppData = AppData
        self.InvestorData = InvestorData
        self.MarketWatchItems = MarketWatchItems

    @classmethod
    def from_json(cls, data: dict):
        return cls(AppData=AppData.from_json(data.pop("AppData")),
                   InvestorData=InvestorData.from_json(data.pop("InvestorData")),
                   MarketWatchItems=MarketWatchData.from_json(data.pop("MarketWatchItems")))


class InstrumentAdded:
    def __init__(self, InstrumentDetailData
                 ):
        self.InstrumentDetailData = InstrumentDetailData

    @classmethod
    def from_json(cls, data: dict):
        return cls(InstrumentDetailData=InstrumentDetailData.from_json(data["InstrumentDetailData"]))


class InstrumentRemoved:
    def __init__(self, InstrumentId):
        self.InstrumentId = InstrumentId

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)
