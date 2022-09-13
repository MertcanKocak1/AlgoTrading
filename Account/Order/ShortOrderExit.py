from binance.enums import *

from Account.Account import Account
from Database.Database import Database
import ClientData

class ShortOrderExit:
    def __init__(self):
        self.acc = Account.getInstance()
        self.database = Database.getInstance()
    def Execute(self):
        # todo Borrowed üzerinden degil Toplayıp ilerlenecek
        try:
            order = self.acc.client.create_margin_order(symbol="BTCUSDT", side=SIDE_BUY, isIsolated='TRUE',
                                                        type=ORDER_TYPE_MARKET,
                                                        sideEffectType="MARGIN_BUY",
                                                        quantity=self.GetTotalBtcToClosePosition())
            order['price'] = self.acc.CalculateWeightedAvg(order)
            order['side'] = "SHORTEXIT"
            order['commission'] = self.acc.SumOfCommission(order)
            ClientData.marginLastPosition = 0
            self.RepayBtcLoan()
            self.database.CreateNewMarginLog(order)
            print(order)
        except Exception as e:
            print("Something Gone Wrong While Exiting Short Exit Position", e)

    def RepayBtcLoan(self):
        try:
            borrowedAmount = self.acc.FloorPrecisionFix(float(self.acc.client.get_isolated_margin_account()['assets'][0]['baseAsset']['borrowed']), 5)
            self.acc.client.repay_margin_loan(asset="BTC", amount=borrowedAmount, symbol="BTCUSDT", isIsolated='TRUE')
            print("RepayLoan Short Order Execute")
        except Exception as e:
            print("Something Gone Wrong While Repaying short exit loan", e)

    def GetTotalBtcToClosePosition(self):
        return self.acc.FloorPrecisionFix(float(self.acc.client.get_isolated_margin_account()['assets'][0]['quoteAsset']['netAssetOfBtc']) / 100 * 99.5, 5)
