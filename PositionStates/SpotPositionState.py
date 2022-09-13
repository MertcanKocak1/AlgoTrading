import time

import ClientData
import PositionStates.PositionContext
import PositionStates.WaitingPositionState
from Account.Account import Account
from Account.Order.SpotOrders.SpotOrder import SpotOrder
from PositionStates.PositionState import PositionState
from StrategyFunctions.StrategyFunctions import StrategyFunctions


class SpotPositionState(PositionState):
    def CheckPosition(self, context):
        acc = Account.getInstance()
        sf = StrategyFunctions.getInstance()

        def GetOutOfPosition(pMessage: str):
            SpotOrder().CreateNewSpotOrder("SELL")
            print(pMessage, time.ctime(), "Price : ", acc.GetLastPositionPrice())
            acc.SetLastPositionPrice(0)
            context.set_state(PositionStates.WaitingPositionState.WaitingPositionState())

        if acc.GetLastPrice() > ClientData.spotLastPosition + ((ClientData.spotLastPosition / 100) * 1.02) \
                or acc.GetLastPrice() < ClientData.spotLastPosition - ((ClientData.spotLastPosition / 100) * 1.02):
            GetOutOfPosition("SL/TP")
            return
        if sf.DummyFunction():
            GetOutOfPosition("Dummy")
            return

