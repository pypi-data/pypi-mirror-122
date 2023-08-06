

class TsTick(object):
    TsCode = ''
    Name = ''
    TradeTime = ''
    PrePrice = ''
    Price = ''
    Open = ''
    High = ''
    Low = ''
    Close = ''
    OpenInt = ''
    Volume = ''
    Amount = ''
    Num = ''
    AskPrice1 = ''
    AskVolume1 = ''
    BidPrice1 = ''
    BidVolume1 = ''
    AskPrice2 = ''
    AskVolume2 = ''
    BidPrice2 = ''
    BidVolume2 = ''
    AskPrice3 = ''
    AskVolume3 = ''
    BidPrice3 = ''
    BidVolume3 = ''
    AskPrice4 = ''
    AskVolume4 = ''
    BidPrice4 = ''
    BidVolume4 = ''
    AskPrice5 = ''
    AskVolume5 = ''
    BidPrice5 = ''
    BidVolume5 = ''

    def to_list(self):
        data = []
        for f in [
            "TsCode",
            "Name",
            "TradeTime",
            "PrePrice",
            "Price",
            "Open",
            "High",
            "Low",
            "Close",
            "OpenInt",
            "Volume",
            "Amount",
            "Num",
            "AskPrice1",
            "AskVolume1",
            "BidPrice1",
            "BidVolume1",
            "AskPrice2",
            "AskVolume2",
            "BidPrice2",
            "BidVolume2",
            "AskPrice3",
            "AskVolume3",
            "BidPrice3",
            "BidVolume3",
            "AskPrice4",
            "AskVolume4",
            "BidPrice4",
            "BidVolume4",
            "AskPrice5",
            "AskVolume5",
            "BidPrice5",
            "BidVolume5"
        ]:
            data.append(getattr(self, f))
        return data


class TsTickIdx(object):
    TsCode = ''
    Name = ''
    TradeTime = ''
    Price = ''
    PreClose = ''
    Open = ''
    High = ''
    Low = ''
    Volume = ''
    Amount = ''

    def to_list(self):
        data = []
        for f in [
            "TsCode",
            "Name",
            "TradeTime",
            "Price",
            "PreClose",
            "Open",
            "High",
            "Low",
            "Volume",
            "Amount"
        ]:
            data.append(getattr(self, f, ''))
        return data


class TsTickOpt(object):
    TsCode = ''
    InstrumentID = ''
    TradeTime = ''
    PrePrice = ''
    Price = ''
    Open = ''
    High = ''
    Low = ''
    Close = ''
    OpenInt = ''
    Volume = ''
    Amount = ''
    Num = ''
    AskPrice1 = ''
    AskVolume1 = ''
    BidPrice1 = ''
    BidVolume1 = ''
    PreDelta = ''
    CurrDelta = ''
    DifPrice1 = ''
    DifPrice2 = ''
    HighLimitPrice = ''
    LowLimitPrice = ''
    ReferPrice = ''

    def to_list(self):
        data = []
        for f in [
            "TsCode",
            "InstrumentID",
            "TradeTime",
            "PrePrice",
            "Price",
            "Open",
            "High",
            "Low",
            "Close",
            "OpenInt",
            "Volume",
            "Amount",
            "Num",
            "AskPrice1",
            "AskVolume1",
            "BidPrice1",
            "BidVolume1",
            "PreDelta",
            "CurrDelta",
            "DifPrice1",
            "DifPrice2",
            "HighLimitPrice",
            "LowLimitPrice",
            "ReferPrice"
        ]:
            data.append(getattr(self, f, ''))
        return data


class TsTickFuture(object):
    TsCode = ''
    InstrumentID = ''
    TradeTime = ''
    PrePrice = ''
    Price = ''
    Open = ''
    High = ''
    Low = ''
    Close = ''
    OpenInt = ''
    Volume = ''
    Amount = ''
    Num = ''
    AskPrice1 = ''
    AskVolume1 = ''
    BidPrice1 = ''
    BidVolume1 = ''
    PreDelta = ''
    CurrDelta = ''
    DifPrice1 = ''
    DifPrice2 = ''
    HighLimitPrice = ''
    LowLimitPrice = ''
    ReferPrice = ''
    PreSettlePrice = ''
    SettlePrice = ''

    def to_list(self):
        data = []
        for f in [
            "TsCode",
            "InstrumentID",
            "TradeTime",
            "PrePrice",
            "Price",
            "Open",
            "High",
            "Low",
            "Close",
            "OpenInt",
            "Volume",
            "Amount",
            "Num",
            "AskPrice1",
            "AskVolume1",
            "BidPrice1",
            "BidVolume1",
            "PreDelta",
            "CurrDelta",
            "DifPrice1",
            "DifPrice2",
            "HighLimitPrice",
            "LowLimitPrice",
            "ReferPrice", 'PreSettlePrice', 'SettlePrice'
        ]:
            data.append(getattr(self, f, ''))
        return data
