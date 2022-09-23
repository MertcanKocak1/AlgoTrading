import math
from typing import Optional

from binance import Client
from numpy import average

import ClientData


class Account:
    __instance = None

    def __init__(self):
        if Account.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.client = Client(ClientData.api_key, ClientData.api_secret)
            Account.__instance = self

    @staticmethod
    def getInstance():
        if Account.__instance is None:
            Account()
        return Account.__instance

    def GetOrderStatus(self, orderId, symbol=ClientData.tradeSymbol) -> bool:
        return self.client.get_margin_order(symbol=symbol, orderId=orderId)['isWorking']

    def GetLoan(self, assetName: str, amount: float) -> None:
        self.client.create_margin_loan(asset=assetName, amount=amount)

    def RepayLoan(self, assetName: str, amount: float) -> None:
        self.client.repay_margin_loan(asset=assetName, amount=amount)

    def GetLastPrice(self, symbol=ClientData.tradeSymbol) -> float:
        return self.FloorPrecisionFix(float(self.client.get_ticker(symbol=symbol)['lastPrice']), 5)

    def GetMaxMarginAmount(self, assetName: str) -> float:
        return self.FloorPrecisionFix(float(
            self.client.get_max_margin_loan(asset=assetName, isolatedSymbol=ClientData.tradeSymbol, isIsolated=True)[
                'amount']), 5)

    @staticmethod
    def FloorPrecisionFix(amount, precision: int):
        return math.floor(amount * 10 ** precision) / 10 ** precision

    def IsClientAlreadyInMarginOrder(self, symbol: str = ClientData.tradeSymbol) -> bool:
        # if client already in order return true otherwise return false
        return not (self.client.get_open_margin_orders(symbol=symbol).__len__() == 0)

    def SpotGetAssetBalance(self, symbol: str = "USDT") -> float:
        return self.FloorPrecisionFix(float(self.client.get_asset_balance(symbol)['free']), 5)

    def GetLastPositionPrice(self, symbol: str = ClientData.tradeSymbol) -> float:
        return self.FloorPrecisionFix(float(self.client.get_my_trades(symbol=symbol)[-1]['price']), 2)

    def GetLast10Position(self, symbol: str = ClientData.tradeSymbol) -> float:
        return self.client.get_my_trades(symbol=symbol)[-30:]

    def GetLastMarginPositionPrice(self, symbol: str = ClientData.tradeSymbol) -> float:
        return self.FloorPrecisionFix(float(self.client.get_margin_trades(symbol=symbol, isIsolated=True)[-1]['price']),
                                      2)

    def SetLastPositionPrice(self, value: Optional[int] = None):
        if value == 0:
            ClientData.spotLastPosition = 0
            return
        ClientData.spotLastPosition = self.GetLastPositionPrice()

    def SumOfCommission(self, order: dict):
        # tek satıra çekilebilir ama böyle daha açıklayıcı
        sum = 0.0
        for fill in order['fills']:
            sum += float(fill['commission'])
        return sum

    def CalculateWeightedAvg(self, order: dict):
        price = []
        weights = []
        for fill in order['fills']:
            price.append(float(fill['price']))
            weights.append(float(fill['qty']))
        return round(average(price, weights=weights), 2)
