import board
import neopixel
import random
import time
from rainbowio import colorwheel
from PixelBuffer import PixelBuffer
from Compositor import Compositor
from Physics import Physics, Particle

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
RED = (220, 0, 0)

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
        return [ DripEffect(self._pixel_buffer_list[i], slowness=1, bounce=True) for i in range(len(self._pixel_buffer_list)) ]


class RainbowEffect:
    def __init__(self, pixel_buffer, slowness=1, brightness=BRIGHTNESS):
        self._pixel_buffer = pixel_buffer
        self._slowness = slowness
        self._brightness = brightness

    def make_generator(self):
        while True:
            for j in range(255):
                for i in range(len(self._pixel_buffer)):
                    rc_index = (i * 256 // len(self._pixel_buffer)) + j
                    self._pixel_buffer[i] = colorwheel(rc_index & 255)
                    for _ in range(self._slowness):
                        yield


class DripEffect:
    """
    Use the physics engine to simulate particles dripping from the top
    """
    def __init__(self, pixel_buffer, slowness=1, brightness=BRIGHTNESS, bounce=True):
        self._pixel_buffer = pixel_buffer
        self._slowness = slowness
        self._brightness = brightness
        self._bounce = bounce

    def make_generator(self, id):
        """
        Create a physics engine to drive movement of particles.
        Regularly toss particles into the "top"
        Map the particle index to a pixel
        Blow up a pixel when it reaches the end of the buffer
        String hangs down from 0 index, so gravity is a positive number
        """
        world = Physics(time=0, g=(0, 25), interval=0.02)
        retire_index = len(self._pixel_buffer) - 1
        while True:
            """
            About 2% of the time, create a random particle at 0 index
            """
            if (world.num_particles() == 0 and random.random() < 0.98):
                Vinit = random.random()*6
                world.add_particle(Particle([0,Vinit], [0,0]))

            world.update_world()

            if self._bounce:
                for i in world.particle_indices(increasing=True):
                    self._pixel_buffer[i] = BLUE
                for i in world.particle_indices(increasing=False):
                    self._pixel_buffer[i] = BLUE
            else:
                for i in world.particle_indices():
                    self._pixel_buffer[i] = BLUE

            # Have particle about to be retired flash RED for a cycle
            if self._pixel_buffer[-1] == BLUE:
                self._pixel_buffer[-1] = RED

            for _ in range(self._slowness):
                yield

            if self._bounce:
                world.bounce_at_limit(retire_index, rebound=0.8)

            world.retire_particles(retire_index, speed_floor=2)

            #print("ID: ", id, world.particle_indices())

            # clear the buffer to redraw next cycle
            for i in range(len(self._pixel_buffer)):
                self._pixel_buffer[i] = OFF





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
    compositor = Compositor()
    buffer_list = [ None ] * FEATHER_WING_ROWS
    for i in range(FEATHER_WING_ROWS):
        buffer_list[i] = PixelBuffer(FEATHER_WING_COLUMNS)

    compositor.bufferList(list_of_buffers=buffer_list)
    #compositor.featherCols(FEATHER_WING_COLUMNS)
    #pixel_buffer=PixelBuffer(FEATHER_WING_COLUMNS)
    pixels = neopixel.NeoPixel(board.GP6, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    compositor.compose(buffer_list, pixels)
    chooser = EffectChooser(pixel_buffer_list=buffer_list)

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

        compositor.compose(buffer_list, pixels)
        pixels.show()
        time.sleep(0.02)
