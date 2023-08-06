

class TsMin(object):
    TsCode = ''
    Freq = ''
    TradeTime = ''
    Open = ''
    Close = ''
    High = ''
    Low = ''
    Volume = ''
    Amount = ''
    OpenInterest = ''

    def to_list(self):
        data = []
        for f in [
            "TsCode",
            "Freq",
            "TradeTime",
            "Open",
            "Close",
            "High",
            "Low",
            "Volume",
            "Amount",
            "OpenInterest"
        ]:
            data.append(getattr(self, f))
        return data
