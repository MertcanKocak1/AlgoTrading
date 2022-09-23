from binance.enums import *

import ClientData
from Account.Account import Account
from Database.Database import Database


class LongOrderExit:
    def __init__(self):
        self.acc = Account.getInstance()
        self.database = Database.getInstance()

    def Execute(self):
        try:
            order = self.acc.client.create_margin_order(symbol=ClientData.tradeSymbol, side=SIDE_SELL,
                                                        isIsolated='TRUE',
                                                        type=ORDER_TYPE_MARKET,
                                                        quantity=self.GetTotalBtc())
            self.RepayUsdt()
            order['price'] = self.acc.CalculateWeightedAvg(order)
            order['side'] = "LONGEXIT"
            order['commission'] = self.acc.SumOfCommission(order)
            ClientData.marginLastPosition = 0
            self.database.CreateNewMarginLog(order)
            print(order)
        except Exception as e:
            print(e)

    def RepayUsdt(self):
        borrowed = self.acc.client.get_isolated_margin_account()['assets'][0]['quoteAsset']['borrowed']
        try:
            self.acc.client.repay_margin_loan(asset="USDT", amount=borrowed, symbol=ClientData.tradeSymbol,
                                              isIsolated='TRUE')
            print("RepayLoan Long Order Executed")
        except Exception as e:
            print("Something Wrong ", e)

    def GetTotalBtc(self) -> float:
        return self.acc.FloorPrecisionFix(
            float(self.acc.client.get_isolated_margin_account()['assets'][0]['baseAsset']['netAsset']), 5)
