"""
Lighting effects rely on some global kinds of configuration and some convenience
variables.
"""
from NeoConfig import *
from Physics import Particle,Physics
#from TapDetector import TapDetector
TapDetectorSupported = False
#from SoundDetector import SoundDetector
SoundDetectorSupported = False
from rainbowio import colorwheel
import random

# move these to NeoConfig to remove duplication
TAP = 3
NO_TAP = 2

class FlipFlopEffect:
    """
    Alternate between half on and half off on the domain
    """
    def __init__(self, pixel_buffer, color=PURPLE, brightness=BRIGHTNESS, slowness=50, name="FlipFlop"):
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
        Make flip and flop over half of the domain
        """
        plen = len(self._pixel_buffer)
        half_len = plen // 2
        while True:
            for p in range(half_len):
                self._pixel_buffer[p] = self._color

            for p in range(half_len, plen):
                self._pixel_buffer[p] = OFF

            for _ in range(self._slowness):
                yield

            for p in range(half_len):
                self._pixel_buffer[p] = OFF

            for p in range(half_len, plen):
                self._pixel_buffer[p] = self._color

            for _ in range(self._slowness):
                yield

class BlinkyEffect:
    """
    Blink all of the pixels in this buffer domain between color and OFF
    """
    def __init__(self, pixel_buffer, color=PURPLE, slowness=100, brightness=BRIGHTNESS):
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


    def make_generator(self):
        """
        Make blinky the default application
        """
        while True:
            for p in range(len(self._pixel_buffer)):
                self._pixel_buffer[p] = self._color

            for _ in range(self._slowness):
                yield

            for p in range(len(self._pixel_buffer)):
                self._pixel_buffer[p] = OFF

            for _ in range(self._slowness):
                yield


class WipeFillEffect:
    """

    """
    def __init__(self, pixel_buffer, color=PURPLE, brightness=BRIGHTNESS, slowness=2):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 20hz using a python generator to break up the updates
        """
        self._pixel_buffer = pixel_buffer
        self._color = color
        self._brightness = brightness
        self._slowness = slowness

    def make_generator(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        for i in range(len(self._pixel_buffer)):
            self._pixel_buffer[i] = self._color
            """
            The yield command here, turns this function into a generator, so it returns after each
            iteration of the loop.   Subsequent calls pick up where they left off.
            """
            for _ in range(self._slowness):
                yield


class SqueezeFillEffect:
    """
    Fills from both directions at the same speed
    *        *
    **      **
    ***    ***
    ****  ****
    **********
    """
    def __init__(self, pixel_buffer, color=PURPLE, slowness=2, brightness=BRIGHTNESS):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 20hz using a python generator to break up the updates
        """
        self._pixel_buffer = pixel_buffer
        self._color = color
        self._slowness = slowness
        self._brightness = brightness

    def make_generator(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        for i in range(len(self._pixel_buffer)):
            self._pixel_buffer[i] = self._color
            self._pixel_buffer[-(i+1)] = self._color
            """
            The yield command here, turns this function into a generator, so it returns after each
            iteration of the loop.   Subsequent calls pick up where they left off.
            """
            for _ in range(self._slowness):
                yield

class RainbowEffect:
    def __init__(self, pixel_buffer, slowness=1, brightness=BRIGHTNESS):
        self._pixel_buffer = pixel_buffer
        self._slowness = slowness
        self._brightness = brightness

    def make_generator(self):
        while True:
            for j in range(255):
                # Do the cycle in six sections to get close to the desired loop deadline
                num_sections = 6
                section_size = len(self._pixel_buffer) // num_sections
                for s in range(num_sections):
                    for i in range(s*section_size, (s+1)*section_size):
                        rc_index = i * 256 // len(self._pixel_buffer) + j
                        self._pixel_buffer[len(self._pixel_buffer) - 1 - i] = colorwheel(rc_index & 255)
                    for _ in range(self._slowness):
                        yield


class DripEffect:
    """
    Use the physics engine to simulate particles dripping from the top
    """
    def __init__(self, pixel_buffer, slowness=1, brightness=BRIGHTNESS, bounce=True, tap=NO_TAP):
        self._pixel_buffer = pixel_buffer
        self._slowness = slowness
        self._brightness = brightness
        self._bounce = bounce
        self._tap = tap
        print("Drip: tap =", self._tap)

    def make_generator(self):
        """
        Create a physics engine to drive movement of particles.
        Regularly toss particles into the "top"
        Map the particle index to a pixel
        Blow up a pixel when it reaches the end of the buffer
        String hangs down from 0 index, so gravity is a positive number
        """
        world = Physics(time=0, g=(0, 50), interval=0.02)
        if TapDetectorSupported:
            td = TapDetector()
        retire_index = len(self._pixel_buffer) - 1
        while True:
            """
            Create a particle on tapping
            About 2% of the time, create a random particle at 0 index
            """
            if TapDetectorSupported and self._tap == TAP:
                td.sense()
                if td.gotTapped():
                     Vinit = random.random()/2
                     world.add_particle(Particle([0,Vinit], [0,0]))
            elif random.random() > 0.97:
                Vinit = random.random()/2
                world.add_particle(Particle([0,Vinit], [0,0]))

            world.update_world()

            if self._bounce:
                for i in world.particle_indices(increasing=True):
                    self._pixel_buffer[i] = BLUE
                for i in world.particle_indices(increasing=False):
                    self._pixel_buffer[i] = RED
            else:
                for i in world.particle_indices():
                    self._pixel_buffer[i] = BLUE

            # Have particle about to be retired flash RED for a cycle
            if self._pixel_buffer[-1] == BLUE:
                self._pixel_buffer[-1] = RED

            for _ in range(self._slowness):
                yield

            if self._bounce:
                world.bounce_at_limit(retire_index, rebound=0.3)

            world.retire_particles(retire_index, speed_floor=4)

            # clear the buffer to redraw next cycle
            for i in range(len(self._pixel_buffer)):
                self._pixel_buffer[i] = OFF


class SoundMeterEffect:

    LIFETIME = 50

    def __init__(self, pixels, color=PURPLE, brightness=BRIGHTNESS, slowness=1):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done all in one shot, suitable for use as a background for some other effect.
        """
        self._pixels = pixels
        self._color = color
        self._brightness = brightness
        self._slowness = slowness
        self._maximum = 0
        self._maxlifetime = 0

    def make_generator(self):

        print('SoundMeterEffect.make_generator')
        if SoundDetectorSupported:
            sd = SoundDetector()
        else:
            LevelAsPixels = len(self._pixels) // 2    # synthetic data starts at midpoint

        while True:

            # get the current sound level from the mic
            # scaled for our pixels
            if SoundDetectorSupported:
                LevelAsPixels = round(sd.getLevelPct() * len(self._pixels))
                if LevelAsPixels >= len(self._pixels):
                    LevelAsPixels = len(self._pixels)-1
            else:
                coin3 = random.random()        # synthetic data.  Flip 3 sided coin.  Equal chance for up, down, same
                if coin3 > 0.66:
                    delta = 1
                elif coin3 > 0.33:
                    delta = -1
                else:
                    delta = 0
                LevelAsPixels = LevelAsPixels + delta
                if LevelAsPixels >= len(self._pixels):               # clamp to max pixel index
                    LevelAsPixels = len(self._pixels) - 1

            #
            # Keep track of maximums, and enforce the
            # lifetime on the recent maximum
            #
            if LevelAsPixels > self._maximum:
                self._maximum = LevelAsPixels-1
                self._maxlifetime = SoundMeterEffect.LIFETIME
            else:
                if self._maxlifetime == 0:
                    self._pixels[self._maximum] = OFF
                    self._maximum = 0
                else:
                    self._maxlifetime-=1

            for p in range(self._maximum):
                self._pixels[p] = OFF
            for p in range(LevelAsPixels):
                self._pixels[p] = self._color

            for _ in range(self._slowness):
                yield



class ClapEffect:
    """
    Use the physics engine to simulate particles dripping from the top
    """
    def __init__(self, pixel_buffer, color=PURPLE, brightness=BRIGHTNESS, slowness=1):
        self._pixel_buffer = pixel_buffer
        self._color = color
        self._brightness = brightness
        self._slowness = slowness

    def clap(self):
        # Build up to the clap event
        # How many cycles should we take to do this?    (48 cps is nicely divisible)

        for i in reversed(range(len(self._pixel_buffer))):
            self._pixel_buffer[0] = ORANGE
            self._pixel_buffer[i] = self._color
            yield
            self._pixel_buffer[0] = ORANGE
            self._pixel_buffer.fill(OFF)
            yield

        for i in range(len(self._pixel_buffer)):
            self._pixel_buffer[i] = ORANGE
        yield from self.rest(4)

        self._pixel_buffer.fill(OFF)
        yield


    def rest(self, duration):
        for _ in range(duration):
            yield

    def make_generator(self):
        """
        """
        while True:
            self._pixel_buffer[0] = ORANGE
            yield
            yield from self.clap()
            yield from self.rest(15)



class InstantFillBackground:

    def __init__(self, pixels, start_index, num_pixels, color=PURPLE, brightness=BRIGHTNESS, slowness=0, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done all in one shot, suitable for use as a background for some other effect.
        """
        self._pixels = pixels
        self._start_index = start_index
        self._num_pixels = num_pixels
        self._pixel_range = pixel_range
        self._color = color
        self._brightness = brightness

    def make_generator(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        p = 0
        for p in self._pixel_range:
            self._pixels[p] = self._color



class RunnerEffect:
    """
    One pixel car drives from low to high on the string.
    This effect does it's own repair of the background.
    That COULD be a service provided by the graphics buffer.
    """
    def __init__(self, pixels, color=BLUE, brightness=100, slowness=2):
        self._pixels = pixels
        self._color = color
        self._slowness = slowness
        self._repair_index = None
        self._repair_value = None

    def make_generator(self):
        """
        Car can run slower, e.g. slowness = 50 to run 1 pixel per second
        Slowess=1 is a bit too hard to see
        """
        while True:
            for carpos in range(len(self._pixels)):

                # repair the damage from the previous frame
                if self._repair_index != None:
                    self._pixels[self._repair_index] = self._repair_value

                # before we draw the car at carpos, save the repair info
                self._repair_index = carpos
                self._repair_value = self._pixels[carpos]

                # draw the car
                self._pixels[carpos] = self._color

                # run at designated speed
                for _ in range(self._slowness):
                    yield

            for carpos in range(len(self._pixels), 0, -1):

                # repair the damage from the previous frame
                if self._repair_index != None:
                    self._pixels[self._repair_index] = self._repair_value

                # before we draw the car at carpos, save the repair info
                self._repair_index = carpos
                self._repair_value = self._pixels[carpos]

                # draw the car
                self._pixels[carpos] = self._color

                # run at designated speed
                for _ in range(self._slowness):
                    yield


class MatrixDisplayMapper:
    """
    Here is the map.   Each element is (row, col)
    --------------------------------------------------------------------------
    (0,0)              (0,1)             ...                   (0, num_cols-1)
    (1,0)              (1,1)             ...                   (1, num_cols-1)
    ...
    (num_rows-2, 0)    (num_rows-2, 1)   ...          (num_rows-2, num_cols-1)
    (num_rows-1, 0)    (num_rows-1, 1)   ...          (num_rows-1, num_cols-1)
    --------------------------------------------------------------------------
    """

    def __init__(self, num_rows, num_cols):
        self._num_rows = num_rows
        self._num_cols = num_cols

    @staticmethod
    def clamp(value, min_val, max_val):
        """Clamps a value within a specified range."""
        return max(min(value, max_val), min_val)


    def rowcol_to_ndx(self, coords):
        # make sure the row and column are in bounds (between 0 and N-1)
        r = MatrixDisplayMapper.clamp(coords[0], 0, self._num_rows-1)
        c = MatrixDisplayMapper.clamp(coords[1], 0, self._num_cols-1)

        # snap row to integer grid so the math works
        return int(round(r)*self._num_cols+c)

    def would_leave_screen(self, coords, vector):
        """
        Return None if the point at coords would leave the screen.
        Otherwise return the new vector resulting from a bounce at the boundary
        """
        row_vect = None
        col_vect = None

        # would leave through the top edge
        if coords[0]+vector[0] < 0:
            row_vect = -vector[0]
        # would leave through the bottom e
        elif coords[0]+vector[0] >= self._num_rows:
            row_vect = -vector[0]

        # would leave through the left edge
        if coords[1]+vector[1] < 0:
            col_vect = -vector[1]
        # would leave through the right edge
        elif coords[1]+vector[1] >= self._num_cols:
            col_vect = -vector[1]

        # if there is no hitting an edge, the vector does not change
        new_row_vect = vector[0] if row_vect is None else row_vect
        new_col_vect = vector[1] if col_vect is None else col_vect

        # if neither hits and edge
        if row_vect is None and col_vect is None:
            return None
        else:
            return (new_row_vect, new_col_vect)


class OnePixelBall:

    def __init__(self, pixels, displaymap, vect=(1, 1), color=BLUE, clear_on_init=False):
        """
        This bouncing ball effect works on a neopixel string or matrix that has a map
        The zero indexed pixel represents the origin at 0,0 (upper right)
        """
        self._pixels = pixels
        self._color = color
        self._vect = vect
        self._rowcol = (0, 0)
        self._displaymap = displaymap
        self._repair_index = None
        self._repair_value = None

    def runner(self, slowness=2):
        #
        #  Ball bounces around forever.
        #
        while True:

            # repair the damage from the previous frame
            if self._repair_index != None:
                self._pixels[self._repair_index] = self._repair_value

            # before we draw the ball at rowcol, save the repair info
            ndx = self._displaymap.rowcol_to_ndx(self._rowcol)
            self._repair_index = ndx
            self._repair_value = self._pixels[ndx]

            # draw the ball at the computed index
            self._pixels[ndx] = self._color

            # see if the ball can move to the next location, or if it bounces at the boundary
            next_vect = self._displaymap.would_leave_screen(self._rowcol, self._vect)

            # if there is a collision, update the new vector
            if not next_vect is None:
                self._vect = next_vect

            # compute the next position for the ball
            next_row = self._rowcol[0] + self._vect[0]
            next_col = self._rowcol[1] + self._vect[1]
            self._rowcol = (next_row, next_col)

            # run at designated speed
            for _ in range(slowness):
                yield


if __name__ == "__main__":

    import time
    import board
    import neopixel

    # Initialize the neopixel model and clear it
    pixels = neopixel.NeoPixel(board.GP6, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    pixels.fill((0,0,0))

    """
    One time setup with solid PURPLE
    """
    print("Display background once")
    purple_background_effect = InstantFillBackground(pixels, color=OFF)

    """
    Bouncing ball effect works in 2D space, so use a display mapper to manage the 2D space
    """
    neofeather = MatrixDisplayMapper(4, 8)
    bounce_effect = OnePixelBall(pixels, displaymap=neofeather, vect=(0.2, 0.3), color=ORANGE, clear_on_init=False)
    do_bouncing_ball = bounce_effect.runner()

    # Draw the background, then wait for a bit to create suspense
    purple_background_effect.run()
    pixels.show()
    time.sleep(3)

    while True:
        # bouncing ball effect runs forever
        next(do_bouncing_ball)
        pixels.show()
        time.sleep(0.02)

