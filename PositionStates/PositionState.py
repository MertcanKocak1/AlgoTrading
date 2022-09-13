from __future__ import annotations

from abc import ABC, abstractmethod

import PositionStates.PositionContext


class PositionState(ABC):
    @abstractmethod
    def CheckPosition(self, context: PositionStates.PositionContext.PositionContext):
        pass
