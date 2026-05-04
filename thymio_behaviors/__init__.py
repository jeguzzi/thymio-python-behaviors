from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Concatenate, ParamSpec, TypeAlias

from .acc import AccBehavior
from .explorer import ExplorerBehavior
from .follower import FollowerBehavior
from .led_acc import LEDAccBehavior
from .led_buttons import LEDButtonsBehavior
from .line import LineFollowingBehavior
from .protocol import ThymioAsebaProtocol
from .prox import LEDProxBehavior
from .prox_comm import LEDProxCommBehavior
from .sound_buttons import SoundButtonsBehavior
from .utils import Chain

P = ParamSpec('P')
Callback: TypeAlias = Callable[Concatenate[ThymioAsebaProtocol, P], None]
Behavior: TypeAlias = Callback[float]


__all__ = [
    'LineFollowingBehavior', 'LEDProxBehavior', 'LEDAccBehavior',
    'LEDButtonsBehavior', 'AccBehavior', 'ExplorerBehavior',
    'FollowerBehavior', 'LEDProxCommBehavior', 'SoundButtonsBehavior', 'Chain',
    'ThymioAsebaProtocol', 'Callback', 'Behavior'
]
