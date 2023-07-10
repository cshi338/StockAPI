from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class lookupResult(_message.Message):
    __slots__ = ["stockPrice", "tradingVolume"]
    STOCKPRICE_FIELD_NUMBER: _ClassVar[int]
    TRADINGVOLUME_FIELD_NUMBER: _ClassVar[int]
    stockPrice: float
    tradingVolume: int
    def __init__(self, stockPrice: _Optional[float] = ..., tradingVolume: _Optional[int] = ...) -> None: ...

class lookupStockName(_message.Message):
    __slots__ = ["stockName"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    def __init__(self, stockName: _Optional[str] = ...) -> None: ...

class tradeResult(_message.Message):
    __slots__ = ["resultTrade"]
    RESULTTRADE_FIELD_NUMBER: _ClassVar[int]
    resultTrade: int
    def __init__(self, resultTrade: _Optional[int] = ...) -> None: ...

class tradeStockName(_message.Message):
    __slots__ = ["stockName", "stockQuantity", "tradeType"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    STOCKQUANTITY_FIELD_NUMBER: _ClassVar[int]
    TRADETYPE_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    stockQuantity: int
    tradeType: str
    def __init__(self, stockName: _Optional[str] = ..., stockQuantity: _Optional[int] = ..., tradeType: _Optional[str] = ...) -> None: ...

class updateResult(_message.Message):
    __slots__ = ["resultUpdate"]
    RESULTUPDATE_FIELD_NUMBER: _ClassVar[int]
    resultUpdate: int
    def __init__(self, resultUpdate: _Optional[int] = ...) -> None: ...

class updateStockName(_message.Message):
    __slots__ = ["stockName", "stockPrice"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    STOCKPRICE_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    stockPrice: float
    def __init__(self, stockName: _Optional[str] = ..., stockPrice: _Optional[float] = ...) -> None: ...
