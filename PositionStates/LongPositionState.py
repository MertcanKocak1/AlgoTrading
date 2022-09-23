import time

import ClientData
import PositionStates.PositionContext
import PositionStates.WaitingPositionState
from Account.Account import Account
from Account.Order.LongOrderExit import LongOrderExit
from PositionStates.PositionState import PositionState
from StrategyFunctions.StrategyFunctions import StrategyFunctions


class LongPositionState(PositionState):
    def CheckPosition(self, context):
        acc = Account.getInstance()
        sf = StrategyFunctions.getInstance()

        def GetOutOfPosition(pMessage: str):
            print(pMessage, time.ctime(), "Price : ", ClientData.marginLastPosition)
            LongOrderExit().Execute()
            context.set_state(PositionStates.WaitingPositionState.WaitingPositionState())

        if acc.GetLastPrice() > ClientData.marginLastPosition + (
                (ClientData.marginLastPosition / 100) * ClientData.takeProfitAmount):
            GetOutOfPosition("Take Profit")
            return
        if acc.GetLastPrice() < ClientData.marginLastPosition - (
                (ClientData.marginLastPosition / 100) * ClientData.stopLossAmount):
            GetOutOfPosition("Stop Loss")
            return
        if sf.DummyFunction():
            GetOutOfPosition("Dummy")
            return
