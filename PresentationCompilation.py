from adafruit_circuitplayground import cp
import board
import neopixel
import random
import time
from PixelBuffer import PixelBuffer
from Compositor import Compositor
from Physics import Physics, Particle
from LightingEffects import WipeFillEffect, SqueezeFillEffect, BlinkyEffect, DripEffect, RainbowEffect

class Presentation:
    """
    A presentation is a collection and configuration of the components necessary to animate,
    render, arrange, and present a responsive lighting effect.
    They include neopixel choice
    """
    def __init__(self, effectList):
        self._compositor = Compositor()
        self._buffer_list = None
        self._buffer = None
        self.effectList = effectList

    def drippingFeatherSeparate(self):
        self._compositor = Compositor()
        pixel_buffer = PixelBuffer(FEATHER_WING_COLUMNS)
        self._buffer_list = [ pixel_buffer ] * FEATHER_WING_ROWS
        #for i in range(FEATHER_WING_ROWS):
        #self._buffer_list[i] = PixelBuffer(FEATHER_WING_COLUMNS)
        self._compositor.bufferList(list_of_buffers=buffer_list)

    def playgroundBuiltIn(self):
        self._buffer = PixelBuffer(CP_PIXELS)
        self._compositor.passThru(CP_PIXELS)

    def sideLight(self):
        self._buffer = PixelBuffer(SIDELIGHT_PIXELS)
        self._compositor.passThru(SIDELIGHT_PIXELS)

    def sideLight7Segment(self):
        sections = 24
        self._buffer = PixelBuffer(sections)
        self._compositor.eightHorizontal(sections)

    def compositor(self):
        return self._compositor

    def pixel_buffer_list(self):
        return self._buffer_list

    def pixel_buffer(self):
        return self._buffer

    def effectList(self):
        return self.effectList

if __name__ == "__main__":
    if _ = 0
        presentation1

    if _ = 1
        presentation2

