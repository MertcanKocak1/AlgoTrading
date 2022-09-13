import time

import ClientData
import PositionStates.LongPositionState
import PositionStates.PositionContext
import PositionStates.ShortPositionState
import PositionStates.SpotPositionState
from Account.Order.LongOrderEntry import LongOrderEntry
from Account.Order.ShortOrderEntry import ShortOrderEntry
from PositionStates.PositionState import PositionState
from StrategyFunctions.StrategyFunctions import StrategyFunctions


class WaitingPositionState(PositionState):
    def CheckPosition(self, context):
        sf = StrategyFunctions.getInstance()
        if sf.DummyFunction():
            print("Long 1. Worked", time.ctime())
            if sf.DummyFunction():
                LongOrderEntry().Execute()
                print("Long 2. Worked", time.ctime(), "And Last Price : ",
                      ClientData.marginLastPosition)
                context.set_state(PositionStates.LongPositionState.LongPositionState())
                return

        if sf.DummyFunction():
            print("Short 1. Worked", time.ctime())
            if sf.DummyFunction():
                ShortOrderEntry().Execute()
                print("2. Worked", time.ctime(), "And Last Price : ", ClientData.marginLastPosition)
                context.set_state(PositionStates.ShortPositionState.ShortPositionState())
            if sf.DummyFunction():
                ShortOrderEntry().Execute()
                print("2. Worked", time.ctime(), "And Last Price : ", ClientData.marginLastPosition)
                context.set_state(PositionStates.ShortPositionState.ShortPositionState())
                return
