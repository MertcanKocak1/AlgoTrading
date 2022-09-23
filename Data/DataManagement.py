import csv
import time
from datetime import datetime
from typing import Tuple

import pandas as pd
import talib
from binance import Client

import ClientData
import PositionStates.PositionContext
from Account.Account import Account


class DataManagement:
    def __init__(self):
        self.client = Account.getInstance().client

        self.positionContext = PositionStates.PositionContext.PositionContext()

    def GetLastKline(self, symbol: str = ClientData.tradeSymbol, timeMinute: int = 5):
        try:
            data = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE,
                                                     f"{timeMinute} Minute Ago GMT+3")[0][0:7]
        except:
            print("Buraya Girdi")
            return self.GetLastKline()
        return data

    def InitilazeAllData(self):
        candlesticks = self.client.get_historical_klines(ClientData.tradeSymbol, Client.KLINE_INTERVAL_5MINUTE,
                                                         "1 Day Ago GMT+3")
        col_names = ['OpeningTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime']
        with open(ClientData.csvDataFileName, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            for candlestick in candlesticks:
                writer.writerow(candlestick)
        f = pd.read_csv(ClientData.csvDataFileName, usecols=[0, 1, 2, 3, 4, 5, 6])
        f.to_csv(ClientData.csvDataFileName, index=False)

    def CalculateRSI(self) -> pd.Series:
        f = pd.read_csv(ClientData.csvDataFileName)
        rsiData = talib.RSI(f['Close'], timeperiod=14)
        result = map(lambda x: "{:.2f}".format(x), rsiData)
        return pd.Series(result)

    def CalculateMACD(self) -> Tuple[pd.Series, pd.Series, pd.Series]:
        f = pd.read_csv(ClientData.csvDataFileName)
        macd, macdsignal, macdhist = talib.MACD(f['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        macd = pd.Series(map(lambda x: "{:.2f}".format(x), macd))
        macdsignal = pd.Series(map(lambda x: "{:.2f}".format(x), macdsignal))
        macdhist = pd.Series(map(lambda x: "{:.2f}".format(x), macdhist))
        return macd, macdsignal, macdhist

    def CalculateStoch(self) -> Tuple[pd.Series, pd.Series]:
        f = pd.read_csv(ClientData.csvDataFileName)
        k, d = talib.STOCH(f['High'], f['Low'], f['Close'])
        k = pd.Series(map(lambda x: "{:.2f}".format(x), k))
        d = pd.Series(map(lambda x: "{:.2f}".format(x), d))
        return k, d

    def RefreshLastRow(self):
        data = pd.read_csv(ClientData.csvDataFileName)
        if self.IsLastKlinePast(int(data.iloc[-1]['CloseTime'])):
            self.AddNewRow()
            if self.positionContext.get_state() == 'WaitingPositionState':
                self.positionContext.AlertThings()
        else:
            lastKline = self.GetLastKline()
            data.iat[-1, 2] = lastKline[2]
            data.iat[-1, 3] = lastKline[3]
            data.iat[-1, 4] = lastKline[4]
            data.iat[-1, 5] = lastKline[5]
            data.to_csv(ClientData.csvDataFileName, index=False)
            self.InitilazeAllIndicators()
            if self.positionContext.get_state() != 'WaitingPositionState':
                self.positionContext.AlertThings()

    def InitilazeAllIndicators(self):
        f = pd.read_csv(ClientData.csvDataFileName)
        f['RSI'] = self.CalculateRSI()
        macd, macdsignal, macdhist = self.CalculateMACD()
        f['MACD'] = macd
        f['MACDSIGNAL'] = macdsignal
        f['MACDHIST'] = macdhist
        k, d = self.CalculateStoch()
        f['STOCHK'] = k
        f['STOCHD'] = d
        f.to_csv(ClientData.csvDataFileName, index=False)

    def AddNewRow(self):
        time.sleep(0.1)
        newKline = self.GetLastKline()
        data = pd.read_csv(ClientData.csvDataFileName)
        oldKline = self.GetLastKline(timeMinute=10)
        data.iat[-1, 2] = oldKline[2]
        data.iat[-1, 3] = oldKline[3]
        data.iat[-1, 4] = oldKline[4]
        data.iat[-1, 5] = oldKline[5]
        data.to_csv(ClientData.csvDataFileName, index=False)
        with open(ClientData.csvDataFileName, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(newKline)
            f.close()
        self.InitilazeAllIndicators()

    def GetCurrentTimeTimestamp(self) -> int:
        return int(datetime.now().timestamp()) * 1000

    def IsLastKlinePast(self, lastKlineCloseTime: int) -> bool:
        return self.GetCurrentTimeTimestamp() > lastKlineCloseTime

    def IsCSVLinesGreaterThan500(self) -> bool:
        df = pd.read_csv(ClientData.csvDataFileName)
        return len(df) > 500
