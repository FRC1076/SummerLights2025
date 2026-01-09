from adafruit_circuitplayground import cp
import board
import neopixel
import random
import time
from PixelBuffer import PixelBuffer
from Compositor import Compositor
from Physics import Physics, Particle
from LightingEffects import WipeFillEffect, SqueezeFillEffect, BlinkyEffect, DripEffect, RainbowEffect

FEATHER_WING_ROWS = 4
FEATHER_WING_COLUMNS = 8

# Two choices for strings
FEATHER_WING_PIXELS = FEATHER_WING_ROWS * FEATHER_WING_COLUMNS
NEON_PIXELS = 64

# Playground onboard neopixels
CP_PIXELS = 10

# Sidelight120
SIDELIGHT_PIXELS = 120

# Choose which we are using
NUM_PIXELS = SIDELIGHT_PIXELS

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
        self._buffer_list = None
        self._buffer = None

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
        return [ DripEffect(self._pixel_buffer, slowness=1) ]







if __name__ == "__main__":

    start_time_ns = time.monotonic_ns()
    # Initialize the neopixel model and clear it using compositor
    presentation = Presentation()
    presentation.sideLight7Segment()
    compositor = presentation.compositor()
    pixel_buffer = presentation.pixel_buffer()

    #Note: for internal pixels on CircuitPlayground import of cp takes care of this
    pixels = neopixel.NeoPixel(board.D10, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    #pixels = cp.pixels
    pixels.auto_write = False
    compositor.compose(pixel_buffer, pixels)
    chooser = EffectChooser(pixel_buffer=pixel_buffer)

    effects = chooser.get_chosen_effects()
    do_effects = [ effect.make_generator() for effect in effects ]

    current_time_ns = time.monotonic_ns()
    elapsed_time_ns = current_time_ns - start_time_ns
    start_time_ns = current_time_ns
    print("Setup took", elapsed_time_ns / 1000000, "milliseconds")
    loop_time_max_ms = 0
    show_time_max_ms = 0
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

        current_time_ns = time.monotonic_ns()
        elapsed_time_ns = current_time_ns - start_time_ns
        start_time_ns = current_time_ns
        loop_time_ms = elapsed_time_ns / 1000000
        if loop_time_ms > loop_time_max_ms:
            loop_time_max_ms = loop_time_ms
            print("Max Looptime: ", loop_time_max_ms, "ms")
        compositor.compose(pixel_buffer, pixels)
        pixels.show()
        current_time_ns = time.monotonic_ns()
        elapsed_time_ns = current_time_ns - start_time_ns
        start_time_ns = current_time_ns
        show_time_ms = elapsed_time_ns / 1000000
        if show_time_ms > show_time_max_ms:
            show_time_max_ms = show_time_ms
            print("Max Showtime: ", show_time_max_ms, "ms")
        adjust = loop_time_ms + show_time_ms
        if adjust < 20:
            time.sleep((20 - adjust)/1000.0)
            #print("INFO: Adjust ", adjust, "milliseconds")
        else:
            print("WARNING: Slip of  ", adjust-20, "milliseconds")

        # rebase start after sleep, since we do not want to count that
        start_time_ns = time.monotonic_ns()

