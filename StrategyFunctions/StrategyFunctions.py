import pandas as pd


class StrategyFunctions:
    __instance = None

    def __init__(self):
        if StrategyFunctions.__instance is not None:
            raise Exception('This Class Singleton')
        else:
            StrategyFunctions.__instance = self

    @staticmethod
    def getInstance():
        if StrategyFunctions.__instance is None:
            StrategyFunctions()
        return StrategyFunctions.__instance

    def IsRsiLowerThan(self, value) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['RSI'] < value

    def IsRsiHigherThan(self, value) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['RSI'] > value

    # Stoch Functions
    # K Blue
    # D Orange
    def IsStochDLowerThan(self, value):
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['STOCHD'] < value

    def IsStochDHigherThan(self, value):
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['STOCHD'] > value

    def IsStochCrossOver(self) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-3]['STOCHK'] > df.iloc[-3]['STOCHD'] and df.iloc[-2]['STOCHK'] < df.iloc[-2]['STOCHD']

    def IsStochCrossUnder(self) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-3]['STOCHK'] < df.iloc[-3]['STOCHD'] and df.iloc[-2]['STOCHK'] > df.iloc[-2]['STOCHD']

    # Macd Functions
    def IsMacdTurnedGreener(self) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['MACDHIST'] >= 0 and df.iloc[-4]['MACDHIST'] > df.iloc[-3]['MACDHIST'] \
               and df.iloc[-3]['MACDHIST'] < df.iloc[-2]['MACDHIST']

    def isMacdTurnedSoftGreener(self) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['MACDHIST'] >= 0 and df.iloc[-3]['MACDHIST'] > df.iloc[-2]['MACDHIST']

    def isMacdTurnedSoftRedder(self) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['MACDHIST'] <= 0 and df.iloc[-3]['MACDHIST'] < df.iloc[-2]['MACDHIST']

    def isMacdTurnedRedder(self) -> bool:
        df = pd.read_csv("5MinuteData.csv")
        return df.iloc[-2]['MACDHIST'] < 0 and df.iloc[-4]['MACDHIST'] < df.iloc[-3]['MACDHIST'] \
               and df.iloc[-3]['MACDHIST'] > df.iloc[-2]['MACDHIST']

    def DummyFunction(self):
        pass