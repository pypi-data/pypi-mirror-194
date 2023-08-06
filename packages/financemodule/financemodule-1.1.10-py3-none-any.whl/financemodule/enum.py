from enum import Enum

class ExchangeRateCurrency(Enum):
    SGD = "SGD"
    HKD = "HKD"
    CNY = "CNY"
    AED = "AED"
    EUR = "EUR"
    USD = "USD"
 



class ExchangeMidrate(Enum):
    SGD_RATE = 0.016
    HKD_RATE = 0.095
    CNY_RATE = 0.083
    AED_RATE = 0.045
    EUR_RATE = 0.011
    USD_RATE = 0.012



class ProgramType(Enum):
    APF = "APF"
    RF = "RF"
    DF = "DF"


class Partytype(Enum):
    ownparty = "ownparty"
    counterparty = "counterparty"


class Accounttype(Enum):
    DEBIT = "D"
    CREDIT = "C"


class InterestType(Enum):
    FIXED = "FIXED"
    FLOATING = "FLOATING"


class FinancingStage(Enum):
    Financing = "Financing"


class CustomerType(Enum):
    customer = "customer"
    non_customer = "non_customer"