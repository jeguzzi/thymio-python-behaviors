from __future__ import annotations

from .protocol import ThymioAsebaProtocol
from .utils import BodyColorPulse, check_grounds, clip_speed, leds_set_body_rgb


class AccBehavior:
    """
    Thymio Acc behavior ported from the
    `firmware <https://github.com/Mobsya/aseba-target-thymio2/blob/master/mode.c#L495>`_,
    see ``static void tick_acc(void)``.

    The original behavior ticks at 50Hz.
    """

    ACC_OBSTACLE: int = 1000
    ACC_FREE_FALL_TRESH: int = 14
    DT: float = 0.02
    SOUND_DISABLE: int = -1
    SOUND_FREEFALL: int = 4
    SOUND_TAP: int = 5

    def __init__(self) -> None:
        self.acc = 32.0
        self.counter: float = 0
        self.body_color_pulse = BodyColorPulse()

    def __call__(self, thymio: ThymioAsebaProtocol, dt: float) -> None:
        acc = thymio.acc
        steps = dt / self.DT
        w = (3 / 4) ** steps
        m_acc = sum(abs(x) for x in acc)
        new_acc = w * self.acc + (1 - w) * m_acc
        play: int | None = None
        if (new_acc > self.ACC_FREE_FALL_TRESH and self.acc <= self.ACC_FREE_FALL_TRESH):
            thymio.leds_top = [15, 0, 0]
            play = self.SOUND_DISABLE
        if (new_acc < self.ACC_FREE_FALL_TRESH and self.acc >= self.ACC_FREE_FALL_TRESH):
            play = self.SOUND_FREEFALL
        self.acc = new_acc
        if self.acc < self.ACC_FREE_FALL_TRESH:
            self.counter += steps
            if self.counter > 5:
                if self.counter >= 10:
                    self.counter = 0
                thymio.leds_top = [32, 0, 0]
            else:
                thymio.leds_top = [0, 0, 0]
        else:
            leds_set_body_rgb(thymio, self.body_color_pulse.get(steps), 0, 0)

        if thymio.acc__tap:
            thymio.acc__tap = 0
            play = self.SOUND_TAP

        prox = thymio.prox_horizontal
        prox_ground_delta = thymio.prox_ground_delta
        if all(prox[i] > self.ACC_OBSTACLE
               for i in (1, 2, 3, 5, 6)) and all(x > 130
                                                 for x in prox_ground_delta):
            thymio.motor_left_target = 0
            thymio.motor_right_target = 0
        elif any(prox[i] > self.ACC_OBSTACLE for i in (0, 1, 2, 3, 4)):
            temp = prox[0] / 5 + prox[1] / 4 + prox[2] / 4 + prox[
                3] / 4 + prox[4] / 5
            temp2 = prox[0] / 6 + prox[1] / 5 - prox[3] / 5 + prox[4] / 6

            thymio.motor_left_target = clip_speed(-(temp + temp2))
            thymio.motor_right_target = clip_speed(temp2 - temp)
        elif any(prox[i] > self.ACC_OBSTACLE for i in (5, 6)):
            thymio.motor_left_target = clip_speed(prox[5] / 4)
            thymio.motor_right_target = clip_speed(prox[6] / 4)
        else:
            thymio.motor_left_target = 0
            thymio.motor_right_target = 0

        check_grounds(thymio)

        if play is not None:
            thymio.call_sound_system(play)
