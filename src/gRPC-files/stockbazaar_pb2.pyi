from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class lookupResult(_message.Message):
    __slots__ = ["stockPrice", "stockQuantity"]
    STOCKPRICE_FIELD_NUMBER: _ClassVar[int]
    STOCKQUANTITY_FIELD_NUMBER: _ClassVar[int]
    stockPrice: float
    stockQuantity: int
    def __init__(self, stockPrice: _Optional[float] = ..., stockQuantity: _Optional[int] = ...) -> None: ...

class lookupStockName(_message.Message):
    __slots__ = ["stockName"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    def __init__(self, stockName: _Optional[str] = ...) -> None: ...

class requestResult(_message.Message):
    __slots__ = ["transactionNum"]
    TRANSACTIONNUM_FIELD_NUMBER: _ClassVar[int]
    transactionNum: int
    def __init__(self, transactionNum: _Optional[int] = ...) -> None: ...

class requestStockName(_message.Message):
    __slots__ = ["stockName", "stockTradeQuantity", "tradeType"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    STOCKTRADEQUANTITY_FIELD_NUMBER: _ClassVar[int]
    TRADETYPE_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    stockTradeQuantity: int
    tradeType: str
    def __init__(self, stockName: _Optional[str] = ..., stockTradeQuantity: _Optional[int] = ..., tradeType: _Optional[str] = ...) -> None: ...

class tradeResult(_message.Message):
    __slots__ = ["resultTrade"]
    RESULTTRADE_FIELD_NUMBER: _ClassVar[int]
    resultTrade: int
    def __init__(self, resultTrade: _Optional[int] = ...) -> None: ...

class tradeStockName(_message.Message):
    __slots__ = ["stockName", "stockTradeQuantity", "tradeType"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    STOCKTRADEQUANTITY_FIELD_NUMBER: _ClassVar[int]
    TRADETYPE_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    stockTradeQuantity: int
    tradeType: str
    def __init__(self, stockName: _Optional[str] = ..., stockTradeQuantity: _Optional[int] = ..., tradeType: _Optional[str] = ...) -> None: ...
