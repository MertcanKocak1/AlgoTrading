# Algo Trading Project

This is a personal algo trading project. This repository educational purpose only. 
In this project i used Singleton and State Design Patterns. 

### Requirements
    pip install pandas
    pip install numpy
    pip install postgres
    pip install python-binance
    pip install TA-Lib
    conda install -c conda-forge ta-liby
After you write your own api keys in ClientData.py, you can start working.

I did not include any strategy so that no one would suffer financial loss. If you want to add your own strategy, you can add your own strategy codes in the WaitingPositionState file. In the WaitingForPosition you can just wrote the conditions for entry to the position. To close your position, you need to write the conditions for exiting in the long or short position state.

If the conditions are met, you need to call the Execute function of the LongOrderEntry class from Account/Order. Here, it borrows from the system itself and when you want to close the position in LongPositionState, the LongOrderExit function pays the debt to the system in the same way.

I'm using PostgreSQL for this project. For create table : 

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
            
 If everything is ready, you can run the Robot.py file and test the system.
