from binance.enums import *

from Account.Account import Account
from Database.Database import Database

import ClientData


class LongOrderEntry:
    def __init__(self):
        self.acc = Account.getInstance()
        self.database = Database.getInstance()

    def Execute(self):
        try:
            self.LoanUsdt()
            lastFree = self.acc.client.get_isolated_margin_account()['assets'][0]['quoteAsset']['free']
            order = self.acc.client.create_margin_order(symbol="BTCUSDT", side=SIDE_BUY, isIsolated='TRUE',
                                                        type=ORDER_TYPE_MARKET,
                                                        quantity=self.TotalBtcToBuy(lastFree))
            order['price'] = self.acc.CalculateWeightedAvg(order)
            order['side'] = "LONGENTRY"
            order['commission'] = self.acc.SumOfCommission(order)
            self.database.CreateNewMarginLog(order)
            ClientData.marginLastPosition = order['price']
            print(order)
        except Exception as e:
            print(e)

    def TotalBtcToBuy(self, total) -> float:
        btcPrice = self.acc.FloorPrecisionFix(float(self.acc.client.get_margin_price_index(symbol='BTCUSDT')['price']),
                                              5)
        return self.acc.FloorPrecisionFix(((float(total) / btcPrice) / 100 * 99), 5)

    def LoanUsdt(self):
        try:
            maxAmount = self.acc.FloorPrecisionFix(self.acc.GetMaxMarginAmount("USDT") / 100 * 98, 3)
            self.acc.client.create_margin_loan(asset="USDT", amount=maxAmount, symbol="BTCUSDT", isIsolated='TRUE')
        except Exception as e:
            print("Something gone wrong when trying take loan", e)
