"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076
https://github.com/FRC1076
"""

from NeoConfig import OFF, PURPLE, BRIGHTNESS
try:
    from TapDetector import TapDetector
    TapDetectorSupported = True
except Exception as e:
    print("Tap Detector not supported: ", str(e))
    TapDetectorSupported = False

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
            Fast = 1 seconds
            Medium = 5 seconds
            Slow = 20 seconds
        """
        for _ in range(self._slowness * 50):
            yield


class TapWaitEffect:
    """
    Do nothing for 5, 25, or 100 seconds.
    """
    def __init__(self, pixel_buffer, color=PURPLE, slowness=20, brightness=BRIGHTNESS, name="TapWait"):
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
        Wait for a tap, or a timeout, whichever comes first
        """
        CYCLES_PER_SECOND = 50
        
        if TapDetectorSupported:
            td = TapDetector()
            
        tap_detected = False
        timeout = self._slowness * CYCLES_PER_SECOND
        
        while not tap_detected and timeout > 0:
            #  Wait for a tap or 
            td.sense()
            if TapDetectorSupported and td.gotTapped():
                tap_detected = True
                
            timeout -= 1
            
            yield
 




