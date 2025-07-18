import board
import neopixel
import time

FEATHER_WING_ROWS = 4
FEATHER_WING_COLUMNS = 8

# Two choices for strings
FEATHER_WING_PIXELS = FEATHER_WING_ROWS * FEATHER_WING_COLUMNS
NEON_PIXELS = 64

# Choose which we are using
NUM_PIXELS = FEATHER_WING_PIXELS

# Useful global constants
COLOR_INC = 255 / NUM_PIXELS                  # color increment to cycle through color range across all pixels
BRIGHTNESS = 0.1

OFF = (0, 0, 0)
PURPLE = (92, 50, 168)
ORANGE = (235, 122, 52)
BLUE = (24, 30, 214)
BUTTERSCOTCH = (252, 186, 3)
GREEN = (3, 252, 92)

class EffectChooser:
    
    def __init__(self, pixels):
        self._pixels = pixels
        pass
        
    def get_chosen_effect(self):
        """
        Currently there is only one effect
        """
        return WipeFillEffect(pixels, 0, 8)
        
    def get_chosen_effects(self):
        """
        Return a list of effects
        """
        return [
                   WipeFillEffect(pixels, 0, 32, color=PURPLE, slowness=2),
                   WipeFillEffect(pixels, 0, 32, color=ORANGE, slowness=4),
                   WipeFillEffect(pixels, 0, 32, color=GREEN, slowness=8)
        ]


class WipeFillEffect:

    def __init__(self, pixels, start_index, num_pixels, color=PURPLE, slowness=2, brightness=BRIGHTNESS, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 50hz using a python generator to break up the updates
        """
        self._pixels = pixels
        self._start_index = start_index
        self._num_pixels = num_pixels
        self._color = color
        self._slowness = slowness
        self._brightness = brightness

        if clear_on_init:
            """
            But, do not display, just zero out everything
            """
            pixels.fill(OFF)

    def make_generator(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        p = self._start_index
        for _ in range(self._num_pixels):
            self._pixels[p] = self._color
            p += 1
            """
            The yield command here, turns this function into a generator, so it returns after each
            iteration of the loop.   Subsequent calls pick up where they left off.
            """
            for _ in range(self._slowness):
                yield


if __name__ == "__main__":

    # Initialize the neopixel model and clear it
    pixels = neopixel.NeoPixel(board.GP6, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    pixels.fill((0,0,0))
    chooser = EffectChooser(pixels)
    
    effects = chooser.get_chosen_effects()
    do_effects = [ effect.make_generator() for effect in effects ]
    print(do_effects)
    next_do_effects = []

    while len(do_effects) > 0 or len(next_do_effects) > 0:
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
                print("Generator stopped: ", do_effect)
        except IndexError:
            # at the end of the list
            # restore it with the list for the next pass
            do_effects = next_do_effects
            next_do_effects = []
            
        pixels.show()
        time.sleep(0.02)
