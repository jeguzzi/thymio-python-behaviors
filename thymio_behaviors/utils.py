from __future__ import annotations

import math
from typing import cast, Generic, ParamSpec
from collections.abc import Callable

from .protocol import ThymioAsebaProtocol

P = ParamSpec("P")


def smod(value: int, n: int) -> int:
    return int((value + 2**(n - 1)) % 2**n - 2**(n - 1))


def umod(value: int, n: int) -> int:
    return int(value % 2**n)


def leds_set_body_rgb(thymio: ThymioAsebaProtocol, r: int, g: int,
                      b: int) -> None:
    thymio.leds_top = [r, g, b]
    thymio.leds_bottom_left = [r, g, b]
    thymio.leds_bottom_right = [r, g, b]


def clip_speed(value: float, max_value: int = 600) -> int:
    return max(-max_value, min(max_value, math.floor(value)))


def check_grounds(thymio: ThymioAsebaProtocol, max_value: int = 130) -> None:
    prox_ground_delta = thymio.prox_ground_delta
    if prox_ground_delta[0] < max_value or prox_ground_delta[1] < max_value:
        thymio.motor_left_target = 0
        thymio.motor_right_target = 0
        thymio.leds_bottom_left = [32, 0, 0]
        thymio.leds_bottom_right = [32, 0, 0]
    else:
        thymio.leds_bottom_left = [0, 0, 0]
        thymio.leds_bottom_right = [0, 0, 0]


class BodyColorPulse:

    def __init__(self) -> None:
        self.led_pulse: float = 0

    def get(self, steps: float) -> int:
        self.led_pulse += steps
        if self.led_pulse > 0:
            ret = self.led_pulse
            if self.led_pulse > 40:
                self.led_pulse = -128
        else:
            ret = -self.led_pulse / 4
        return math.floor(ret)


def _rainbow_get(i: int) -> int:
    if i < 32:
        return i
    if i < 64:
        return 64 - i
    return 0


class Rainbow:

    def __init__(self) -> None:
        self.led_i: float = 0

    def get(self, steps: float) -> tuple[int, int, int]:
        self.led_i = self.led_i + steps
        if self.led_i > 96:
            self.led_i = 0
        r = self.led_i
        g = self.led_i + 32
        if g > 96:
            g -= 96
        b = self.led_i + 64
        if b > 96:
            b -= 96
        return cast('tuple[int, int, int]',
                    tuple(_rainbow_get(math.floor(x)) for x in (r, g, b)))


class Chain(Generic[P]):
    """
    A sequence of homogeneous callable objects
    that are evaluate in sequence.

    For example ::

       chain = Chain(obj_1, obj_2)
       chain(*args, **kwargs)

    will internally call ::

       obj_1(*args, **kwargs)
       obj_2(*args, **kwargs)
    """

    def __init__(self, *items: Callable[P, None]) -> None:
        self._items = items

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Calls the items in sequence"""
        for c in self._items:
            c(*args, **kwargs)
