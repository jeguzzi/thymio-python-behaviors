from __future__ import annotations

import math

from .protocol import ThymioAsebaProtocol


def aseba_atan2(y: int, x: int) -> int:
    return int(round(math.atan2(y, x) / math.pi * (2 ** 15)))


class LEDAccBehavior:
    """
    Thymio Acc behavior ported from the
    `firmware <https://github.com/Mobsya/aseba-target-thymio2/blob/master/behavior.c#L306>`_,
    see ``static void behavior_leds_acc(void)``.

    The original behavior ticks at 50Hz.
    """

    def __init__(self) -> None:
        self.previous_led = -1

    def __call__(self, thymio: ThymioAsebaProtocol, dt: float) -> None:
        led = -1
        intensity = 0
        if thymio.acc[2] < 21:
            ha = aseba_atan2(thymio.acc[0], thymio.acc[1]) / 2
            if ha >= -2000 and ha < 2000:
                led = 28
            elif ha < -2000 and ha >= -6000:
                led = 27
            elif ha < -6000 and ha >= -10000:
                led = 26
            elif ha < -10000 and ha >= -14000:
                led = 25
            elif ha < -14000 and ha >= 14000:
                led = 24
            elif ha < 6000 and ha >= 2000:
                led = 36
            elif ha < 10000 and ha >= 6000:
                led = 37
            elif ha < 14000 and ha >= 10000:
                led = 31
            intensity = max(0, 42 - abs(thymio.acc[2]) * 2)
            if abs(thymio.acc[0]) + abs(thymio.acc[1]) <= 10:
                intensity = 0
        if self.previous_led != led:
            if self.previous_led >= 0:
                thymio.call__leds_set(self.previous_led, 0)
            if led >= 0:
                thymio.call__leds_set(led, intensity)
        self.previous_led = led
