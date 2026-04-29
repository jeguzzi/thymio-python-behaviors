from __future__ import annotations

import numpy as np

from .protocol import ThymioAsebaProtocol


class LEDProxCommBehavior:
    """
    TODO
    """

    def __init__(self) -> None:
        self.max = np.full((7, ), 3800)
        self.min = np.full((7, ), 1700)
        self.d: float = 0

    def __call__(self, thymio: ThymioAsebaProtocol, dt: float) -> None:
        for _, values in thymio.prox_comm_buffer:
            intensities = np.asarray(values)
            self.d = 11
            not_zero = intensities > 0
            self.max = np.maximum(intensities, self.max)
            self.min[not_zero] = np.minimum(intensities[not_zero],
                                            self.min[not_zero])
            vs = np.clip((intensities - self.min) / (self.max - self.min), 0, 1)
            t = np.floor(vs * 32).astype(np.int16)
            thymio.call_leds_circle(t[2], t[3], t[4], t[6], 0, t[5], t[0],
                                    t[1])
            thymio.call_leds_buttons(0, 0, 32, 0)
        self.d -= dt / 0.01
        if self.d <= 0:
            thymio.call_leds_circle(0, 0, 0, 0, 0, 0, 0, 0)
            thymio.call_leds_buttons(0, 0, 0, 0)
