import psycopg2
import pandas as pd


class Database:
    __instance = None

    def __init__(self):
        if Database.__instance is not None:
            raise Exception('This Class Singleton')
        else:
            self.conn = psycopg2.connect(
                database="BinanceAlgoTrading", user='postgres', password='mertcan', host='127.0.0.1', port='5432'
            )
            self.cursor = self.conn.cursor()
            Database.__instance = self

    @staticmethod
    def getInstance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def closeConnection(self):
        self.conn.close()

    """
    create table SpotLogs(
          spot_log_id serial primary key
        , symbol varchar(20)
        , clientOrderId float
        , tstamp float
        , price float
        , qty varchar(50)
        , quoteQty varchar(50)
        , tip varchar(20)
        , side varchar(20)
        , rsi float
        , sar float
        , macdhist float
        , macd float 
        , macdSignal float 
        , stochk float
        , stochd float
        )
    """

    def CreateNewSpotLog(self, order: dict, data) -> None:
        self.cursor = self.conn.cursor()
        sqlInsertCode = '''insert into spotlogs(symbol, clientOrderId, tStamp, 
                                    price,qty,quoteQty, 
                                    tip,side, rsi, 
                                    sar, macdhist, macd, 
                                    macdSignal, stochk, stochd) values (%s, %s, %s, 
                                    %s,%s, %s, 
                                    %s,%s, %s, 
                                    %s, %s,%s, 
                                    %s, %s, %s)'''
        self.cursor.execute(sqlInsertCode, (order['symbol']
                                            , order['clientOrderId']
                                            , order['transactTime']
                                            , order['price']
                                            , order['quantity']
                                            , order['quoteOrderQty']
                                            , order['status']
                                            , order['type']
                                            , order['side']
                                            , data['RSI']
                                            , data['SAR']
                                            , data['MACDHIST']
                                            , data['MACD']
                                            , data['MACDSIGNAL']
                                            , data['STOCHK']
                                            , data['STOCHD']))
        self.conn.commit()

    """
    Margin Log Creation PostgreSQL Code
        create table MarginLog(
          margin_log_id serial primary key
        , symbol varchar(20)
        , order_id float
        , price float
        , qty varchar(50)
        , quoteQty varchar(50)
        , commission float
        , side varchar(20)
        , isIsolated bool
        , tstamp float
        )
    """

    def CreateNewMarginLog(self, order: dict) -> None:
        self.cursor = self.conn.cursor()
        sqlInsertCode = '''insert into MarginLog(symbol, order_id, price, 
                                       qty, quoteQty, commission,side, isIsolated, tstamp) values (%s, %s, %s, %s,%s, %s, %s, %s, %s)'''
        self.cursor.execute(sqlInsertCode, (order['symbol']
                                            , order['orderId']
                                            , order['price']
                                            , order['executedQty']
                                            , order['cummulativeQuoteQty']
                                            , order['commission']
                                            , order['side']
                                            , order['isIsolated']
                                            , order['transactTime']))
        self.conn.commit()

    """ PostgreSQL Backtest Create Table SQL Code
    create table backtest(
              backtest_id serial primary key
            , side varchar(20)
            , closethis float
            , close1 float
            , rsi float
            , rsi1 float
            , macd float
            , macd1 float
            , macd2 float
            , macdsignal float
            , macdsignal1 float
            , macdsignal2 float
    	    , macdhist float
            , macdhist1 float
            , macdhist2 float
            , stochk float
            , stochk1 float
            , stochd float
            , stochd1 float
            , sar float
            , sar1 float
            , startmoney float
            , startTime varchar(100)
    )"""

    def CreateBacktestLog(self, order: dict):
        self.cursor = self.conn.cursor()
        sqlInsertCode = '''insert into backtest(side, closethis, close1
                , rsi, rsi1, macd
                , macd1, macd2, macdsignal
                , macdsignal1, macdsignal2, macdhist
                , macdhist1, macdhist2, stochk
                , stochk1, stochd, stochd1, 
                sar , sar1, startmoney,
                startTime) values (%s, %s, %s, 
                                            %s,%s, %s, 
                                            %s,%s, %s, 
                                            %s, %s,%s, 
                                            %s, %s, %s,
                                            %s, %s, %s,
                                            %s, %s, %s, %s)'''
        self.cursor.execute(sqlInsertCode, (order['SIDE']
                                            , order['Close']
                                            , order['Close1']
                                            , order['RSI']
                                            , order['RSI1']
                                            , order['MACD']
                                            , order['MACD1']
                                            , order['MACD2']
                                            , order['MACDSIGNAL']
                                            , order['MACDSIGNAL1']
                                            , order['MACDSIGNAL2']
                                            , order['MACDHIST']
                                            , order['MACDHIST1']
                                            , order['MACDHIST2']
                                            , order['STOCHK']
                                            , order['STOCHK1']
                                            , order['STOCHD']
                                            , order['STOCHD1']
                                            , order['SAR']
                                            , order['SAR1']
                                            , order['StartMoney']
                                            , order['OpeningTime']
                                            ))
        self.conn.commit()

    def CreateSQLQueryToDataFrame(self, queryString: str) -> pd.DataFrame:
        self.cursor = self.conn.cursor()
        self.cursor.execute(queryString)
        column_names = [i[0] for i in self.cursor.description]
        return pd.DataFrame(self.cursor.fetchall(), columns=column_names)
