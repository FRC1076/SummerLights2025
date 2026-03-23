"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076
https://github.com/FRC1076
"""

from NeoConfig import OFF, PURPLE, BRIGHTNESS

class WaitEffect:
    """
    Do nothing for 5, 25, or 100 seconds.
    """
    def __init__(self, pixel_buffer, color=PURPLE, slowness=20, brightness=BRIGHTNESS, name="Wait"):
        """
        Base class for lighting effects
        Could be useful for documentation, or maybe actually used as a base class
        Note, this relies on constants from elsewhere.    Should probably import them instead of assuming
        they have been imported.
        """
        self._pixel_buffer = pixel_buffer
        self._color = color
        self._slowness = slowness
        self._brightness = brightness
        self._name=name

    def make_generator(self):
        """
        Do nothing but take a certain amount of time to run
        Demo uses fast=1, medium=5, and slow=20
        Multiply by 250 to get:
            Fast = 5 seconds
            Medium = 25 seconds
            Slow = 100 seconds
        """
        for _ in range(self._slowness * 250):
            yield




