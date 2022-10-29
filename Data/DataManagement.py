import csv
import sys
import time
from datetime import datetime
from typing import Tuple, Optional

import pandas as pd
import talib
from binance import Client

import ClientData
import PositionStates.PositionContext
from Account.Account import Account

sys.setrecursionlimit(10 ** 8)

class DataManagement:
    def __init__(self):
        self.client = Account.getInstance().client

        self.positionContext = PositionStates.PositionContext.PositionContext()

    def GetLastKline(self, symbol: str = ClientData.tradeSymbol, timeMinute: int = 1):
        try:
            data = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE,
                                                     f"{timeMinute} Minute Ago GMT+3")[0][0:7]
        except:
            print("Buraya Girdi")
            return self.GetLastKline()
        return data

    def InitilazeAllData(self):
        candlesticks = self.client.get_historical_klines(ClientData.tradeSymbol, Client.KLINE_INTERVAL_1MINUTE,
                                                         "2 Hour GMT+3")
        col_names = ['OpeningTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime']
        with open(ClientData.csvDataFileName, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            for candlestick in candlesticks:
                writer.writerow(candlestick)
        f = pd.read_csv(ClientData.csvDataFileName, usecols=[0, 1, 2, 3, 4, 5, 6])
        f.to_csv(ClientData.csvDataFileName, index=False)

    def TwoAfterComma(self, data: pd.Series):
        return "{:.2f}".format(data)

    def CalculateRSI(self, f: pd.DataFrame) -> pd.Series:
        rsiData = talib.RSI(f['Close'], timeperiod=14)
        result = rsiData.apply(self.TwoAfterComma)
        return result

    def CalculateSAR(self, f: pd.DataFrame) -> pd.Series:
        sarData = talib.SAR(f['High'], f['Low'])
        result = sarData.apply(self.TwoAfterComma)
        return result

    def CalculateMACD(self, f: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series]:
        macd, macdsignal, macdhist = talib.MACD(f['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        macd = macd.apply(self.TwoAfterComma)
        macdsignal = macdsignal.apply(self.TwoAfterComma)
        macdhist = macdhist.apply(self.TwoAfterComma)
        return macd, macdsignal, macdhist

    def CalculateStoch(self, f: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        k, d = talib.STOCH(f['High'], f['Low'], f['Close'])
        k = k.apply(self.TwoAfterComma)
        d = d.apply(self.TwoAfterComma)
        return k, d

    def RefreshLastRow(self):
        data = pd.read_csv(ClientData.csvDataFileName)
        if self.IsLastKlinePast(int(data.iloc[-1]['CloseTime'])):
            self.AddNewRow()
            if self.positionContext.get_state() == 'WaitingPositionState':
                self.positionContext.AlertThings()
        else:
            lastKline = self.GetLastKline()
            data = self.InitializeLastRow(data, lastKline)
            data.to_csv(ClientData.csvDataFileName, index=False)
            time.sleep(0.1)
            self.InitilazeAllIndicators()
            if self.positionContext.get_state() != 'WaitingPositionState':
                self.positionContext.AlertThings()

    def InitilazeAllIndicators(self, dataLength: Optional = None):
        if dataLength is not None:
            # this is not working i tried sending last 50 value and try to get last 50 rsi value it should work but calculations are coming wrong
            f = pd.read_csv(ClientData.csvDataFileName).iloc[-dataLength:]
            rsi = self.CalculateRSI(f).iloc[-2:]
            macdHolder = self.CalculateMACD(f)
            macd, macdsignal, macdhist = macdHolder[0].iloc[-1], macdHolder[1].iloc[-1], macdHolder[2].iloc[-1]
            stochHolder = self.CalculateStoch(f)
            k, d = stochHolder[0].iloc[-1], stochHolder[1].iloc[-1]
            sar = self.CalculateSAR(f).iloc[-1]
            del f
            f = pd.read_csv(ClientData.csvDataFileName)
            f.at[f.index[-1], 'RSI'] = rsi
            f.at[f.index[-1], 'MACD'] = macd
            f.at[f.index[-1], 'MACDSIGNAL'] = macdsignal
            f.at[f.index[-1], 'MACDHIST'] = macdhist
            f.at[f.index[-1], 'STOCHK'] = k
            f.at[f.index[-1], 'STOCHD'] = d
            f.at[f.index[-1], 'SAR'] = sar
        else:
            f = pd.read_csv(ClientData.csvDataFileName)
            f['RSI'] = self.CalculateRSI(f)
            macd, macdsignal, macdhist = self.CalculateMACD(f)
            k, d = self.CalculateStoch(f)
            sar = self.CalculateSAR(f)
            f['MACD'] = macd
            f['MACDSIGNAL'] = macdsignal
            f['MACDHIST'] = macdhist
            f['STOCHK'] = k
            f['STOCHD'] = d
            f['SAR'] = sar
        f.to_csv(ClientData.csvDataFileName, index=False)

    def AddNewRow(self):
        time.sleep(0.1)
        newKline = self.GetLastKline()
        data = pd.read_csv(ClientData.csvDataFileName)
        oldKline = self.GetLastKline(timeMinute=2)
        data = self.InitializeLastRow(data, oldKline)
        data.to_csv(ClientData.csvDataFileName, index=False)
        with open(ClientData.csvDataFileName, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(newKline)
            f.close()
        time.sleep(0.1)
        self.InitilazeAllIndicators()

    def InitializeLastRow(self, df: pd.DataFrame, kline: pd.Series) -> pd.DataFrame:
        df.at[df.index[-1], 'Open'] = kline[1]
        df.at[df.index[-1], 'High'] = kline[2]
        df.at[df.index[-1], 'Low'] = kline[3]
        df.at[df.index[-1], 'Close'] = kline[4]
        return df

    def GetCurrentTimeTimestamp(self) -> int:
        return int(datetime.now().timestamp()) * 1000

    def IsLastKlinePast(self, lastKlineCloseTime: int) -> bool:
        return self.GetCurrentTimeTimestamp() > lastKlineCloseTime

    def IsCSVLinesGreaterThan(self, value) -> bool:
        df = pd.read_csv(ClientData.csvDataFileName)
        return len(df) > value
