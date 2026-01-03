import board
import neopixel
import time
from rainbowio import colorwheel
from PixelBuffer import PixelBuffer
from Compositor import Compositor

FEATHER_WING_ROWS = 4
FEATHER_WING_COLUMNS = 8

# Two choices for strings
FEATHER_WING_PIXELS = FEATHER_WING_ROWS * FEATHER_WING_COLUMNS
NEON_PIXELS = 64

# Choose which we are using
NUM_PIXELS = FEATHER_WING_PIXELS

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


class EffectChooser:
    """
    
    """

    def __init__(self, pixel_buffer):
        self._pixels = pixel_buffer
        pass

    def get_chosen_effects(self):
        """
        Return a list of effects
        """
        return  [   WipeFillEffect(self._pixels[0:32], color=PINK, slowness=1),
                    SqueezeFillEffect(self._pixels[0:16], color=PURPLE, slowness=10),
                    SqueezeFillEffect(self._pixels[16:16], color=ORANGE, slowness=20) ]


class RainbowEffect:    
    def __init__(self, pixel_buffer, color=PURPLE, slowness=2, brightness=BRIGHTNESS, clear_on_init=True):
        self._pixel_buffer = pixel_buffer
        self._slowness = slowness
        self._brightness = brightness

    def make_generator(self):
        for j in range(255):
            for i in range(self._pixel_buffer.len):
                rc_index = (i * 256 // self._pixel_buffer.len) + j
                self._pixel_buffer[i] = colorwheel(rc_index & 255)
                for _ in range(self._slowness):
                    yield


class WipeFillEffect:
    """
    
    """
    def __init__(self, pixel_buffer, color=PURPLE, slowness=2, brightness=BRIGHTNESS, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 20hz using a python generator to break up the updates
        """
        self._pixel_buffer = pixel_buffer
        self._color = color
        self._slowness = slowness
        self._brightness = brightness

        if clear_on_init:
            """
            But, do not display, just zero out everything
            """
            pixel_buffer.fill(OFF)

    def make_generator(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        for i in range(self._pixel_buffer.len):
            self._pixel_buffer[i] = color
            """
            The yield command here, turns this function into a generator, so it returns after each
            iteration of the loop.   Subsequent calls pick up where they left off.
            """
            for _ in range(self._slowness):
                yield


if __name__ == "__main__":

    # Initialize the neopixel model and clear it using compositor
    compositor = Compositor().passThru(NUM_PIXELS)
    pixel_buffer=PixelBuffer(NUM_PIXELS)
    pixels = neopixel.NeoPixel(board.GP6, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    compositor.compose(pixel_buffer, pixels)
    chooser = EffectChooser(pixel_buffer)

    effects = chooser.get_chosen_effects()
    do_effects = [ effect.make_generator() for effect in effects ]
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
