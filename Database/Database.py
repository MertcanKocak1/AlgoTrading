import psycopg2


class Database:
    __instance = None

    def __init__(self):
        if Database.__instance is not None:
            raise Exception('This Class Singleton')
        else:
            self.conn = psycopg2.connect(
                database="BinanceAlgoTrading", user='postgres', password='--', host='127.0.0.1', port='5432'
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


    def CreateNewSpotLog(self, order: dict) -> None:
        self.cursor = self.conn.cursor()
        sqlInsertCode = '''insert into spotlogs(symbol, clientOrderId, tStamp, 
                                    price, status, tip,side) values (%s, %s, %s, %s,%s, %s, %s)'''
        self.cursor.execute(sqlInsertCode, (order['symbol']
                                            , order['clientOrderId']
                                            , order['transactTime']
                                            , order['price']
                                            , order['status']
                                            , order['type']
                                            , order['side']))
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
