import PositionStates.PositionState
import PositionStates.WaitingPositionState


class PositionContext:
    _state = None

    def __init__(self):
        self.set_state(PositionStates.WaitingPositionState.WaitingPositionState())

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state.__class__.__name__

    def AlertThings(self):
        self._state.CheckPosition(self)
