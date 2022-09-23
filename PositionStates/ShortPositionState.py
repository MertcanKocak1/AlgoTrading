import time

import ClientData
import PositionStates.PositionContext
import PositionStates.WaitingPositionState
from Account.Account import Account
from Account.Order.ShortOrderExit import ShortOrderExit
from PositionStates.PositionState import PositionState
from StrategyFunctions.StrategyFunctions import StrategyFunctions


class ShortPositionState(PositionState):
    def CheckPosition(self, context):
        acc = Account.getInstance()
        sf = StrategyFunctions.getInstance()

        def GetOutOfPosition(pMessage: str):
            print(pMessage, time.ctime(), "Price : ", ClientData.marginLastPosition)
            ShortOrderExit().Execute()
            context.set_state(PositionStates.WaitingPositionState.WaitingPositionState())

        if acc.GetLastPrice() > ClientData.marginLastPosition + (
                (ClientData.marginLastPosition / 100) * ClientData.takeProfitAmount):
            GetOutOfPosition("Stop Loss")
            return
        if acc.GetLastPrice() < ClientData.marginLastPosition - (
                (ClientData.marginLastPosition / 100) * ClientData.stopLossAmount):
            GetOutOfPosition("Take Profit")
            return
        if sf.DummyFunction():
            GetOutOfPosition("Dummy")
            return
