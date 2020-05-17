import inspect
import json
from enum import Enum


class ErrorObject(object):
    def __init__(self, i: int, m: str):
        self.i = i
        self.m = m

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class OrderType(Enum):
    Buy = 1
    Sale = 2


class OrderValidity(Enum):
    Day = 1
    GoodTillCancelled = 2
    GoodTillDate = 3
    FillAndKill = 4


class OrderCreditSource(Enum):
    Broker = 1
    Saman = 2
    Melat = 3


class Date:
    def __init__(self, Year, Month, Day):
        self.Year = Year
        self.Month = Month
        self.Day = Day

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class OrderStatus(Enum):
    Created = 1
    Active = 2
    Executed = 3
    Canceled = 4
    Error = 5
    PartialExecuted = 6


class OrderLockType(Enum):
    UnLock = 1
    LockForCreate = 2
    LockForEdit = 3
    LockForCancel = 4


class OrderSource(Enum):
    Web = 1
    Notification = 2
    Algorithmic = 3
    API = 4
    Admin = 5
    InitialOffering = 6
    Backoffice = 7
    Old = 8
    Mobile = 9


class StateChangeData:
    def __init__(self, Id, OrderStatus: OrderStatus, HON, Edited, OrderLockType: OrderLockType, BlockedCredit, Remain,
                 OrderSource: OrderSource):
        self.Id = Id
        self.OrderStatus = OrderStatus
        self.HON = HON
        self.Edited = Edited
        self.OrderLockType = OrderLockType
        self.BlockedCredit = BlockedCredit
        self.Remain = Remain
        self.OrderSource: OrderSource = OrderSource

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            OrderStatus=OrderStatus(data.pop("OrderStatus")),
            OrderLockType=OrderLockType(data.pop("OrderLockType")),
            OrderSource=OrderSource(data.pop("OrderSource")),
            **data
        )


class InvestorOptionStatus(Enum):
    Normal = 1
    AtRisk = 2
    MarginCall = 3


class AccountInfo:
    def __init__(self, BuyPower, AccountRemain, Credit, Block, OptionStatus):
        self.BuyPower = BuyPower
        self.AccountRemain = AccountRemain
        self.Credit = Credit
        self.Block = Block
        self.OptionStatus = OptionStatus

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class BestLimitData:
    def __init__(self, Level, BuyOrderCount, BuyPrice, BuyVolume, SellOrderCount, SellPrice, SellVolume):
        self.Level = Level
        self.BuyOrderCount = BuyOrderCount
        self.BuyPrice = BuyPrice
        self.BuyVolume = BuyVolume
        self.SellOrderCount = SellOrderCount
        self.SellPrice = SellPrice
        self.SellVolume = SellVolume

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class NscState(Enum):
    NotProvided = 1
    Authorized = 2
    AuthorizedFrozen = 3
    AuthorizedSuspended = 4
    AuthorizedReserved = 5
    Forbidden = 6
    ForbiddenFrozen = 7
    ForbiddenSuspended = 8
    ForbiddenReserved = 9

    NscStateMap = {
        "I ": Forbidden,
        "IG": ForbiddenFrozen,
        "IS": ForbiddenSuspended,
        "IR": ForbiddenReserved,
        "A ": Authorized,
        "AG": AuthorizedFrozen,
        "AS": AuthorizedSuspended,
        "AR": AuthorizedReserved,
    }

    @staticmethod
    def ToNscState(string):
        return NscState.NscStateMap[string]


class TradePercentChange:
    def __init__(self,
                 ActualBuyCount,
                 ActualBuyQuantity,
                 ActualSellCount,
                 ActualSellQuantity,
                 LegalBuyCount,
                 LegalBuyQuantity,
                 LegalSellCount,
                 LegalSellQuantity):
        self.ActualBuyCount = ActualBuyCount
        self.ActualBuyQuantity = ActualBuyQuantity
        self.ActualSellCount = ActualSellCount
        self.ActualSellQuantity = ActualSellQuantity
        self.LegalBuyCount = LegalBuyCount
        self.LegalBuyQuantity = LegalBuyQuantity
        self.LegalSellCount = LegalSellCount
        self.LegalSellQuantity = LegalSellQuantity

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class BourseContractData:
    def __init__(self, Size,
                 StartDate,
                 EndDate,
                 InitialMargin):
        self.Size = Size
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.InitialMargin = InitialMargin

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class InstrumentDetailData:
    def __init__(self,
                 Id,
                 NumberOfTrades,
                 MarketQuanity,
                 LastTradePrice,
                 FinalPrice,
                 LastTradeDate,
                 SectorPE,
                 NoData,
                 FirstPrice,
                 ThresholdHigh,
                 ThresholdLow,
                 BaseVolume,
                 YesterdayLastTradePrice,
                 YesterdayFinalPrice,
                 MaxValidBuyVolume,
                 MaxValidSellVolume,
                 MinValidVolume,
                 LowestPrice,
                 HighestPrice,
                 NscState,
                 InsCode,
                 TradePercentChageData,
                 EstimatedEPS,
                 BourseContractData
                 ):
        self.Id = Id
        self.NumberOfTrades = NumberOfTrades
        self.MarketQuanity = MarketQuanity
        self.LastTradePrice = LastTradePrice
        self.FinalPrice = FinalPrice
        self.LastTradeDate = LastTradeDate
        self.SectorPE = SectorPE
        self.NoData = NoData
        self.FirstPrice = FirstPrice
        self.ThresholdHigh = ThresholdHigh
        self.ThresholdLow = ThresholdLow
        self.BaseVolume = BaseVolume
        self.YesterdayLastTradePrice = YesterdayLastTradePrice
        self.YesterdayFinalPrice = YesterdayFinalPrice
        self.MaxValidBuyVolume = MaxValidBuyVolume
        self.MaxValidSellVolume = MaxValidSellVolume
        self.MinValidVolume = MinValidVolume
        self.LowestPrice = LowestPrice
        self.HighestPrice = HighestPrice
        self.NscState = NscState
        self.InsCode = InsCode
        self.TradePercentChangeData = TradePercentChageData
        self.EstimatedEPS = EstimatedEPS
        self.BourseContractData = BourseContractData

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            TradePercentChageData=TradePercentChange.from_json(data.pop("TradePercentChangeData")),
            BourseContractData=BourseContractData.from_json(data.pop("BourseContractData")),
            **data
        )


class InstrumentWageType(Enum):
    NotSet = 0
    Bourse = 1
    ExtraBourse = 2
    JointShare = 3
    BaseExtraBourse = 4
    BourseETF = 5
    ExtraBourseETF = 6
    AccessoryOption = 7
    Salaf = 8
    BourseOption = 9


class MarketwatchInstrumentDetailData:
    def __init__(self, InstrumentDetailData, BestLimit):
        self.InstrumentDetailData = InstrumentDetailData
        self.BestLimit = BestLimit

    @classmethod
    def from_json(cls, data: dict):
        return cls(InstrumentDetailData=InstrumentDetailData.from_json(data.pop("InstrumentDetailData")),
                   BestLimit=BestLimitData.from_json(data.pop("BestLimit")))


class MarketOverallStatistics:
    def __init__(self, OverallIndex,
                 OverallIndexPercent,
                 TotalTradeCount,
                 TotalTradePrice,
                 TotalTradeQuantity,
                 CowFactor):
        self.OverallIndex = OverallIndex
        self.OverallIndexPercent = OverallIndexPercent
        self.TotalTradeCount = TotalTradeCount
        self.TotalTradePrice = TotalTradePrice
        self.TotalTradeQuantity = TotalTradeQuantity
        self.CowFactor = CowFactor

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class InvestorData:
    def __init__(self,
                 InvestorInfo,
                 MarketWatchs,
                 OrderDatas,
                 AssetData,
                 Theme,
                 Basket,
                 Setting,
                 HasBaseMarketRiskAgreement,
                 PositionDataArray
                 ):
        self.InvestorInfo = InvestorInfo
        self.MarketWatchs = MarketWatchs
        self.OrderDatas = OrderDatas
        self.AssetData = AssetData
        self.Theme = Theme
        self.Basket = Basket
        self.Setting = Setting
        self.HasBaseMarketRiskAgreement = HasBaseMarketRiskAgreement
        self.PositionDataArray = PositionDataArray

    @classmethod
    def from_json(cls, data: dict):
        return cls(InvestorInfo=InvestorInfo.from_json(data.pop("InvestorInfo")),
                   MarketWatchs=list(map(MarketWatch.from_json, data.pop("MarketWatchs"))),
                   OrderDatas=list(map(OrderData.from_json, data.pop("OrderDatas"))),
                   AssetData=list(map(AssetData.from_json, data.pop("AssetData"))),
                   PositionDataArray=list(map(PositionDataArray.from_json, data.pop("PositionDataArray"))), **data)


class InvestorInfo:
    def __init__(self,
                 InvestorId,
                 FName,
                 LName,
                 AccountInfo,
                 CanBlockFromSaman,
                 CanBlockFromMellat,
                 CanUseSamanGateway,
                 CanUseMellatGateway,
                 BankAccountList,
                 TMP,
                 BourseCode,
                 MaxOrderRepeat,
                 CanUsePaymentGateway,
                 ):
        self.InvestorId = InvestorId
        self.FName = FName
        self.LName = LName
        self.AccountInfo = AccountInfo
        self.CanBlockFromSaman = CanBlockFromSaman
        self.CanBlockFromMellat = CanBlockFromMellat
        self.CanUseSamanGateway = CanUseSamanGateway
        self.CanUseMellatGateway = CanUseMellatGateway
        self.BankAccountList = BankAccountList
        self.TMP = TMP
        self.BourseCode = BourseCode
        self.MaxOrderRepeat = MaxOrderRepeat
        self.CanUsePaymentGateway = CanUsePaymentGateway

    @classmethod
    def from_json(cls, data: dict):
        return cls(AccountInfo=AccountInfo.from_json(data.pop("AccountInfo")),
                   BankAccountList=list(map(BankAccount.from_json, data.pop("BankAccountList"))), **data)


class BankAccount:
    def __init__(self, code,
                 Name):
        self.code = code
        self.Name = Name

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class MarketWatch:
    def __init__(self, code,
                 Name):
        self.code = code
        self.Name = Name

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class MarketWatchData:
    def __init__(self, Id,
                 Name, MarketwatchInstrumentDetailDataArray):
        self.Id = Id
        self.Name = Name
        self.MarketwatchInstrumentDetailDataArray = MarketwatchInstrumentDetailDataArray

    @classmethod
    def from_json(cls, data: dict):
        return cls(MarketwatchInstrumentDetailDataArray=MarketwatchInstrumentDetailData.from_json(
            data.pop("MarketwatchInstrumentDetailDataArray")), **data)


class OrderData:
    def __init__(self, Id,
                 InstrumentId,
                 CreateDate,
                 Quantity,
                 Price,
                 ExecutedQuantity,
                 OrderSide,
                 Validity,
                 OrderValidityDate,
                 OrderStatus,
                 CreditSource,
                 HON,
                 Edited,
                 OrderLockType,
                 DisclosedQuantity,
                 MinimumQuantity,
                 IsToday,
                 BlockedCredit,
                 Remain,
                 Error,
                 OrderSource,
                 ExtraData
                 ):
        self.Id = Id
        self.InstrumentId = InstrumentId
        self.CreateDate = CreateDate
        self.Quantity = Quantity
        self.Price = Price
        self.ExecutedQuantity = ExecutedQuantity
        self.OrderSide = OrderSide
        self.Validity = Validity
        self.OrderValidityDate = OrderValidityDate
        self.OrderStatus = OrderStatus
        self.CreditSource = CreditSource
        self.HON = HON
        self.Edited = Edited
        self.OrderLockType = OrderLockType
        self.DisclosedQuantity = DisclosedQuantity
        self.MinimumQuantity = MinimumQuantity
        self.IsToday = IsToday
        self.BlockedCredit = BlockedCredit
        self.Remain = Remain
        self.Error = Error
        self.OrderSource = OrderSource
        self.ExtraData = ExtraData

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            OrderStatus=OrderStatus(data.pop("OrderStatus")),
            OrderSide=OrderType(data.pop("OrderSide")),
            Validity=OrderValidity(data.pop("Validity")),
            OrderLockType=OrderLockType(data.pop("OrderLockType")),
            OrderSource=OrderSource(data.pop("OrderSource")),
            OrderValidityDate=Date.from_json(data.pop("OrderValidityDate")),
            CreditSource=OrderCreditSource.from_json(data.pop("CreditSource")),
            **data)


class AssetData:
    def __init__(self, Id,
                 Quantity,
                 Price,
                 LastTradePrice):
        self.Id = Id
        self.Quantity = Quantity
        self.Price = Price
        self.LastTradePrice = LastTradePrice

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class Theme(Enum):
    Light = 0
    Dark = 1
    Custom = 3


class AppData:
    def __init__(self, AppVersion,
                 Date,
                 StringDate,
                 Time,
                 MarketOverallStatistics):
        self.AppVersion = AppVersion
        self.Date = Date
        self.StringDate = StringDate
        self.Time = Time
        self.MarketOverallStatistics = MarketOverallStatistics

    @classmethod
    def from_json(cls, data: dict):
        return cls(Date=Date.from_json(data.pop("Date")),
                   MarketOverallStatistics=MarketOverallStatistics.from_json(data.pop("MarketOverallStatistics")),
                   **data)


# TODO: changed Date to StringDate
class ReportType(Enum):
    Normal = 1
    Aggregated = 2
    Balanced = 3


class OrderListReportDetailResult:
    def __init__(self, TradeNumber,
                 TradeDate,
                 TradeQuantity,
                 TradePrice,
                 BrokerWage,
                 BurseWage,
                 DepositAgencyWage,
                 ExchangeWage,
                 TechnologyWage,
                 Tax,
                 TotalPrice):
        self.TradeNumber = TradeNumber
        self.TradeDate = TradeDate
        self.TradeQuantity = TradeQuantity
        self.TradePrice = TradePrice
        self.BrokerWage = BrokerWage
        self.BurseWage = BurseWage
        self.DepositAgencyWage = DepositAgencyWage
        self.ExchangeWage = ExchangeWage
        self.TechnologyWage = TechnologyWage
        self.Tax = Tax
        self.TotalPrice = TotalPrice

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class PositionDataArray:
    def __init__(self, InstrumentId,
                 Asset,
                 buyOrder,
                 saleOrder,
                 InitialMarginCount,
                 InitialMarginAmount,
                 MarginCount,
                 MarginAmount):
        self.InstrumentId = InstrumentId
        self.Asset = Asset
        self.buyOrder = buyOrder
        self.saleOrder = saleOrder
        self.InitialMarginCount = InitialMarginCount
        self.InitialMarginAmount = InitialMarginAmount
        self.MarginCountWage = MarginCount
        self.MarginAmount = MarginAmount

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif isinstance(obj, Enum):
            return obj.value
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)

        return obj
