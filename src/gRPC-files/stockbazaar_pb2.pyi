from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class followersAssigned(_message.Message):
    __slots__ = ["followerOne", "followerTwo"]
    FOLLOWERONE_FIELD_NUMBER: _ClassVar[int]
    FOLLOWERTWO_FIELD_NUMBER: _ClassVar[int]
    followerOne: str
    followerTwo: str
    def __init__(self, followerOne: _Optional[str] = ..., followerTwo: _Optional[str] = ...) -> None: ...

class followersResult(_message.Message):
    __slots__ = ["resultFollowers"]
    RESULTFOLLOWERS_FIELD_NUMBER: _ClassVar[int]
    resultFollowers: int
    def __init__(self, resultFollowers: _Optional[int] = ...) -> None: ...

class lookupOrderNum(_message.Message):
    __slots__ = ["orderNum"]
    ORDERNUM_FIELD_NUMBER: _ClassVar[int]
    orderNum: int
    def __init__(self, orderNum: _Optional[int] = ...) -> None: ...

class lookupOrderNumResult(_message.Message):
    __slots__ = ["orderNum", "stockName", "stockTradeQuantity", "tradeType"]
    ORDERNUM_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    STOCKTRADEQUANTITY_FIELD_NUMBER: _ClassVar[int]
    TRADETYPE_FIELD_NUMBER: _ClassVar[int]
    orderNum: int
    stockName: str
    stockTradeQuantity: int
    tradeType: str
    def __init__(self, orderNum: _Optional[int] = ..., stockName: _Optional[str] = ..., tradeType: _Optional[str] = ..., stockTradeQuantity: _Optional[int] = ...) -> None: ...

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

class propagateOrderNum(_message.Message):
    __slots__ = ["orderNum", "stockName", "stockTradeQuantity", "tradeType"]
    ORDERNUM_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    STOCKTRADEQUANTITY_FIELD_NUMBER: _ClassVar[int]
    TRADETYPE_FIELD_NUMBER: _ClassVar[int]
    orderNum: int
    stockName: str
    stockTradeQuantity: int
    tradeType: str
    def __init__(self, orderNum: _Optional[int] = ..., stockName: _Optional[str] = ..., tradeType: _Optional[str] = ..., stockTradeQuantity: _Optional[int] = ...) -> None: ...

class propagateResult(_message.Message):
    __slots__ = ["resultPropagate"]
    RESULTPROPAGATE_FIELD_NUMBER: _ClassVar[int]
    resultPropagate: int
    def __init__(self, resultPropagate: _Optional[int] = ...) -> None: ...

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

class synchronizeTransNum(_message.Message):
    __slots__ = ["orderNum", "synchronizedAdd"]
    ORDERNUM_FIELD_NUMBER: _ClassVar[int]
    SYNCHRONIZEDADD_FIELD_NUMBER: _ClassVar[int]
    orderNum: int
    synchronizedAdd: str
    def __init__(self, orderNum: _Optional[int] = ..., synchronizedAdd: _Optional[str] = ...) -> None: ...

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

class transNumInfo(_message.Message):
    __slots__ = ["orderNum", "stockName", "stockTradeQuantity", "tradeType"]
    ORDERNUM_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    STOCKTRADEQUANTITY_FIELD_NUMBER: _ClassVar[int]
    TRADETYPE_FIELD_NUMBER: _ClassVar[int]
    orderNum: int
    stockName: str
    stockTradeQuantity: int
    tradeType: str
    def __init__(self, orderNum: _Optional[int] = ..., stockName: _Optional[str] = ..., tradeType: _Optional[str] = ..., stockTradeQuantity: _Optional[int] = ...) -> None: ...
