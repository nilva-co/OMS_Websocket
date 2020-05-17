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


class InvestorOptionStatus(Enum):
    Normal = 1
    AtRisk = 2
    MarginCall = 3


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


class Theme(Enum):
    Light = 0
    Dark = 1
    Custom = 3


class ReportType(Enum):
    Normal = 1
    Aggregated = 2
    Balanced = 3


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
