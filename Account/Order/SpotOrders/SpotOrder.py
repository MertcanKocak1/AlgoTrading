from Account.Account import Account
from Database.Database import Database
import time


class SpotOrder:
    def __init__(self):
        self.acc = Account.getInstance()
        self.database = Database.getInstance()

    def CreateNewSpotOrder(self, side, symbol: str = 'BTCUSDT'):
        if side == "BUY":
            balance = self.acc.SpotGetAssetBalance()
            btcPrice = self.acc.GetLastPrice()
            quantity = self.acc.FloorPrecisionFix((balance / btcPrice), 5)
            try:
                order = self.acc.client.order_market_buy(
                    symbol=symbol,
                    quantity=quantity)
                order['price'] = self.acc.GetLastPositionPrice()
                print(order)
                self.database.CreateNewSpotLog(order)
            except Exception as e:
                print('Spot Buy Order Creating Fail!', e, time.ctime())
        elif side == "SELL":
            quantity = self.acc.SpotGetAssetBalance("BTC")
            try:
                order = self.acc.client.order_market_sell(
                    symbol=symbol,
                    quantity=quantity)
                order['price'] = self.acc.GetLastPositionPrice()
                print(order)
                self.database.CreateNewSpotLog(order)
            except Exception as e:
                print('Spot SELL Order Creating Fail!', e, time.ctime())
