import adafruit_circuitplayground.bluefruit as cp
import board
#import neopixel
import random
import time
from rainbowio import colorwheel
from PixelBuffer import PixelBuffer
from Compositor import Compositor
from Physics import Physics, Particle
from LightingEffects import WipeFillEffect, SqueezeFillEffect, BlinkyEffect, DripEffect

FEATHER_WING_ROWS = 4
FEATHER_WING_COLUMNS = 8

# Two choices for strings
FEATHER_WING_PIXELS = FEATHER_WING_ROWS * FEATHER_WING_COLUMNS
NEON_PIXELS = 64

# Playground onboard neopixels
CP_PIXELS = 10

# Choose which we are using
NUM_PIXELS = CP_PIXELS

# Useful global constants

# color increment ensures that we can cycle through a full
# range of color intensities from the first to last pixels
COLOR_INC = 255 / NUM_PIXELS

# keep things dim to save power
BRIGHTNESS = 0.1

# some ready made colors (feel free to add more)
OFF = (0, 0, 0)
PURPLE = (92, 50, 168)
ORANGE = (235, 122, 52)
BLUE = (24, 30, 214)
BUTTERSCOTCH = (252, 186, 3)
GREEN = (3, 252, 92)
PINK = (248, 3, 252)
RED = (220, 0, 0)

class Presentation:
    """
    A presentation is a collection and configuration of the components necessary to animate,
    render, arrange, and present a responsive lighting effect.
    They include neopixel choice
    """
    def __init__(self):
        self._compositor = Compositor()

    def drippingSeparate(self):
        self._compositor = Compositor()
        self._buffer_list = [ None ] * FEATHER_WING_ROWS
        for i in range(FEATHER_WING_ROWS):
            self._buffer_list[i] = PixelBuffer(FEATHER_WING_COLUMNS)
        compositor.bufferList(list_of_buffers=buffer_list)

    def playgroundBuiltIn(self):
        self._buffer = PixelBuffer(CP_PIXELS)
        compositor.passThru(CP_PIXELS)



class EffectChooser:
    """

    """
    def __init__(self, pixel_buffer=None, pixel_buffer_list=None):
        """
        Usually pass in a pixel_buffer, but when there are multiple buffers to be combined by the Compositor,
        there will be a list of buffers that could be passed to the effect.    Can specify only 1 or a list.
        Not both.
        """
        self._pixel_buffer = pixel_buffer
        self._pixel_buffer_list = pixel_buffer_list
        pass

    def get_chosen_effects(self):
        """
        Return a list of effects
        return  [   WipeFillEffect(PixelBuffer(self._pixel_buffer[0:32]), color=PINK, slowness=1),
                    SqueezeFillEffect(PixelBuffer(self._pixel_buffer[0:16]), color=PURPLE, slowness=10),
                    SqueezeFillEffect(PixelBuffer(self._pixel_buffer[16:16]), color=ORANGE, slowness=20) ]
        """
        return [ DripEffect(self._pixel_buffer, slowness=1, bounce=True) ]







if __name__ == "__main__":

    # Initialize the neopixel model and clear it using compositor
    compositor = Compositor()
    pixel_buffer = PixelBuffer(NUM_PIXELS)
    compositor.passThru(NUM_PIXELS)

    #pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    compositor.compose(pixel_buffer, cp.pixels)
    chooser = EffectChooser(pixel_buffer=pixel_buffer)

    effects = chooser.get_chosen_effects()
    do_effects = [ effect.make_generator(id) for id,effect in enumerate(effects) ]
    next_do_effects = []
    while len(do_effects) > 0 or len(next_do_effects) > 0:

        all_live_effects_have_run_once = False

        while not all_live_effects_have_run_once:

            try:
                """
                Remove the effect from the front of the list.  If it runs without stopping,
                put it at the end of the list to be used on the next pass through the effects
                """
                do_effect = do_effects.pop(0)
                try:
                    next(do_effect)
                    next_do_effects.append(do_effect)
                except StopIteration:
                    pass
            except IndexError:
                # at the end of the list
                # restore it with the list for the next pass
                do_effects = next_do_effects
                next_do_effects = []
                all_live_effects_have_run_once = True

        compositor.compose(pixel_buffer, pixels)
        pixels.show()
        time.sleep(0.02)
# Write your code here :-)
