import ClientData

from binance.enums import *

from Database.Database import Database

from Account.Account import Account
from Account.Order.Order import Order


class ShortOrderEntry(Order):
    def __init__(self):
        self.acc = Account.getInstance()
        self.database = Database.getInstance()

    def Execute(self):
        try:
            order = self.acc.client.create_margin_order(symbol="BTCUSDT", side=SIDE_SELL, type="MARKET",
                                                        quantity=self.MaxBTCAmount(), sideEffectType="MARGIN_BUY",
                                                        isIsolated=True)
            order['price'] = self.acc.CalculateWeightedAvg(order)
            order['side'] = "SHORTENTRY"
            order['commission'] = self.acc.SumOfCommission(order)
            self.database.CreateNewMarginLog(order)
            ClientData.marginLastPosition = order['price']
            print(order)
        except Exception as e:
            print("Something Went Wrong While Entering Short Enter Position", e)

    def MaxBTCAmount(self):
        return self.acc.FloorPrecisionFix(self.acc.GetMaxMarginAmount("BTC") / 100 * 99, 5)
