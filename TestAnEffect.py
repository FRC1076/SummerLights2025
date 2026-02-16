import board
import neopixel
import time
from PixelBuffer import PixelBuffer
from FlipFlopEffect import FlipFlopEffect


KEYBOAR_PIN = board.D2
PLAYGROUND_PIN = board.D10
NEO_PIN = PLAYGROUND_PIN

FEATHER_WING_ROWS = 4
FEATHER_WING_COLUMNS = 8

# Two choices for strings
FEATHER_WING_PIXELS = FEATHER_WING_ROWS * FEATHER_WING_COLUMNS
NEON_PIXELS = 64

# Playground onboard neopixels
CP_PIXELS = 10

# Sidelight120
SIDELIGHT_PIXELS = 120

# Sidelight60
# SIDELIGHT_PIXELS = 60

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
BUTTERSCOTCH = (253, 100, 10)
GREEN = (3, 252, 3)
PINK = (248, 3, 252)
RED = (220, 0, 0)


class EffectChooser:
    """

    """
    def __init__(self, pixels):
        self._pixels = pixels
        pass

    def get_chosen_effects(self):
        """
        Return a list of effects
        """
        return  [ FlipFlopEffect(self._pixels, color=RED, slowness=25) ]



if __name__ == "__main__":

    # Initialize the neopixel model and clear it
    pixels = neopixel.NeoPixel(NEO_PIN, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    pixels.fill((0,0,0))
    pixels.show()

    pixel_buffer = PixelBuffer(NUM_PIXELS)
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

        for i in range(len(pixel_buffer)):
            pixels[i]=pixel_buffer[i]
        pixels.show()
        time.sleep(0.02)
