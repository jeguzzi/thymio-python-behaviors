from __future__ import annotations

import numpy as np

from .protocol import ThymioAsebaProtocol


class LEDButtonsBehavior:
    """
    Thymio LED prox behavior ported from the
    `firmware <https://github.com/Mobsya/aseba-target-thymio2/blob/master/behavior.c#L182>`_,
    see ``static void behavior_leds_buttons(void)``.

    The original behavior ticks at 50Hz.
    """

    DT: float = 0.02

    def __init__(self) -> None:
        self.button_counter = np.zeros(5)

    def __call__(self, thymio: ThymioAsebaProtocol, dt: float) -> None:
        steps = dt / self.DT
        # TODO:
        values = np.array([
            thymio.button_backward, thymio.button_left, thymio.button_center,
            thymio.button_forward, thymio.button_right
        ], dtype=bool)
        self.button_counter[values] = np.minimum(
            32, self.button_counter[values > 0] + 3 * steps)
        self.button_counter[~values] = 0
        bc = self.button_counter.astype(int)
        if bc[2]:
            leds = bc[[2, 2, 2, 2]]
        else:
            leds = bc[[3, 4, 0, 1]]
        thymio.call_leds_buttons(*leds)
