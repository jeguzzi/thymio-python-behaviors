from __future__ import annotations

from .protocol import ThymioAsebaProtocol


class SoundButtonsBehavior:
    """
    Thymio LED prox behavior ported from the
    `firmware <https://github.com/Mobsya/aseba-target-thymio2/blob/master/behavior.c#L225>`_,
    see ``static void behavior_sound_buttons(void)``.

    The original behavior ticks at 50Hz.
    """

    def __init__(self) -> None:
        self.buttons = [0] * 5
        self.sounds = [2, 2, 3, 2, 2]

    def __call__(self, thymio: ThymioAsebaProtocol, dt: float) -> None:
        buttons = [
            thymio.button_backward, thymio.button_left, thymio.button_center,
            thymio.button_forward, thymio.button_right
        ]
        for sound, state, prev in zip(self.sounds, buttons, self.buttons, strict=True):
            if state and state != prev:
                thymio.call_sound_system(sound)
                break
        self.buttons = buttons
