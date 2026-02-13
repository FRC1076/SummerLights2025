#from adafruit_circuitplayground import cp
import board
import neopixel
import random
import time
from PixelBuffer import PixelBuffer
from Compositor import Compositor
from Physics import Physics, Particle
from LightingEffects import RunnerEffect, FlipFlopEffect, WipeFillEffect, SqueezeFillEffect, BlinkyEffect, DripEffect, RainbowEffect, ClapEffect

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
#SIDELIGHT_PIXELS = 60

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
GREEN = (3, 252, 92)
PINK = (248, 3, 252)
RED = (220, 0, 0)

TAP = 3
NO_TAP = 2

ValidSpeeds =   {"slow" :   20,
                 "medium" :  5,
                 "fast" :    1,
                 "tap" :     TAP,
                 "no-tap" :  NO_TAP}

ValidColors =   {"off": OFF,
                 "purple" : PURPLE,
                 "orange" : ORANGE,
                 "butterscotch" : BUTTERSCOTCH,
                 "blue" : BLUE,
                 "red"  : RED,
                 "green" :  GREEN
                }

ValidEffects = [ "clear",                 #  clear the display (shortcut with simple reset)
                 "flipflop",              #  switch between two adjacent lights
                 "wipe",                  #  display purple on the whole string
                 "rainbow",               #  rainbow effect on full string
                 "runner",                #  zip back and forth
                 "fliprunner",            #  for the frameNcorners (flip on corners, run sides)
                 "squeeze",               #  close the curtain
                 "multi",                 #  several effects on substrings
                 "drip",                  #  physics based particle animation
                 "Quit" ]

ValidDivisions = [   "2",                  #  2 divisions
                     "3",                  #  3 divisions of equal size
                     "4",                  #
                     "5",                  #
                     "6",                  #  6 sections of equal size
                     "12",                 #  12 divisions of equal size
                     "30",                 #  30 divisions of 4
                     "60"  ]               #  60 divisions of equal size

ValidCompositors = [ "full",               #  pass-thru, single buffer, simplest layout
                     "oval",               #  sliced topology for oval with start/end at top
                     "7segment",           #  sliced 7segment display (figure eight)
                     "frameNcorners",      #  5-buffer layout with sides contiguous
                     "1/2",                #  split into two pixels
                     "1/4",                #  split into four pixels
                     "1/10" ] + ValidDivisions



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

    def sideLightGroups(self, num_groups=2):
        """
        This should work cleanly with 2, 3, 5, 4, 6 and their products.
        """
        self._buffer = PixelBuffer(num_groups)
        self._compositor.groupsOfN(SIDELIGHT_PIXELS, num_groups)


    def sideLightDivisions(self, num_divisions=2):
        """
        This should work cleanly with 2, 3, 5, 4, 6 and their products.
        """
        #self._buffer_list = [ PixelBuffer(SIDELIGHT_PIXELS // num_divisions) for i in range(num_divisions) ]
        # Note: compositor creates the buffers
        self._compositor.divisionsOfN(SIDELIGHT_PIXELS, num_divisions)

    def sideLight7Segment(self):
        groups = 24
        self._buffer = PixelBuffer(groups)
        self._compositor.eightHorizontal(groups)

    def oval(self):
        groups = NUM_PIXELS // 2
        self._buffer = PixelBuffer(groups)
        self._compositor.oval(NUM_PIXELS, groups)

    def frameNcorners(self):
        """
        This only works for 60 pixel string
        """
        self._buffer_list = [ PixelBuffer(5) for i in range(4) ] + [ PixelBuffer(40) ]
        self._compositor.frameNCorners()

    def compositor(self):
        return self._compositor

    def pixel_buffer_list(self):
        return self._compositor.buffer_list()

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
        assert pixel_buffer is None or pixel_buffer_list is None, "Specify buffer or buffer_list, not both"
        self._pixel_buffer = pixel_buffer
        self._pixel_buffer_list = pixel_buffer_list
        pass

    def get_effect_name(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[0]
        except:
            name = None
        return name

    def get_effect_comp_name(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[1]
        except:
            name = None
        return name

    def get_effect_color(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[2]
            color = ValidColors[name]
        except:
            color = PURPLE
        return color

    def get_effect_speed(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[3]
            speed = ValidSpeeds[name]
        except:
            speed = 1
        return speed

    def get_chosen_effects(self, effect_cmd):
        """
        Return a list of effects to run simultaneously.
        """
        if self._pixel_buffer_list is not None:
            print("get_chosen_effects: len(buffer_list):", len(self._pixel_buffer_list))
        if self._pixel_buffer is not None:
            print("get_chosen_effects: len(buffer:", len(self._pixel_buffer))
        effect_name = self.get_effect_name(effect_cmd)
        comp_name = self.get_effect_comp_name(effect_cmd)
        color = self.get_effect_color(effect_cmd)
        speed = self.get_effect_speed(effect_cmd)
        print("Name:", effect_name, "Comp:", comp_name, "Color:", color, "Speed:", speed)

        if effect_name == "wipe" and comp_name == "full":
            return [ WipeFillEffect(self._pixel_buffer, color=color, slowness=speed) ]
        elif effect_name == "flipflop":
            div_names = ValidDivisions
            if comp_name == "full":
                return [ FlipFlopEffect(self._pixel_buffer, color=color, slowness=speed) ]
            elif comp_name in div_names:
                divs = int(comp_name)
                return [ FlipFlopEffect(self._pixel_buffer_list[i], color=color, slowness=speed, name="FlipFlop"+str(i)) for i in range(divs) ]
            elif comp_name == "oval":
                return [ FlipFlopEffect(self._pixel_buffer, color=color, slowness=speed) ]
        elif effect_name == "squeeze":
            div_names = ValidDivisions
            if comp_name == "full":
                return [ SqueezeFillEffect(self._pixel_buffer, color=color, slowness=speed) ]
            elif comp_name in div_names:
                divs = int(comp_name)
                return [ SqueezeFillEffect(self._pixel_buffer_list[i], color=color, slowness=speed) for i in range(divs) ]

        elif effect_name == "clear" and comp_name == "all":
            return [ WipeFillEffect(self._pixel_buffer, color=OFF, slowness=1) ]
        elif effect_name == "multi" and comp_name == "4":
            return [ RainbowEffect(self._pixel_buffer_list[0], slowness=5),
                     WipeFillEffect(self._pixel_buffer_list[1], color=BUTTERSCOTCH, slowness=10),
                     RunnerEffect(self._pixel_buffer_list[2], color=color, slowness=speed),
                     FlipFlopEffect(self._pixel_buffer_list[3], color=ORANGE, slowness=10) ]
        elif effect_name == "rainbow" and comp_name == "full":
            return [ RainbowEffect(self._pixel_buffer, slowness=10) ]
        elif effect_name == "runner":
            div_names = ValidDivisions
            if comp_name == "full" or comp_name == "oval" or comp_name == "7segment":
                return [ RunnerEffect(self._pixel_buffer, color=color, slowness=speed) ]
            elif comp_name in div_names:
                divs = int(comp_name)
                return [ RunnerEffect(self._pixel_buffer_list[i], color=color, slowness=speed) for i in range(divs) ]
        elif effect_name == "drip":
            if comp_name == "full" or comp_name == "oval":
                """
                borrow the speed part of the command to enable tap on drip
                """
                return [ DripEffect(self._pixel_buffer, slowness=1, tap=speed) ]

        elif effect_name == "fliprunner":
            if comp_name == "frameNcorners":
                re = [ RunnerEffect(self._pixel_buffer_list[5], color=color, slowness=speed) ]
                return re + [ FlipFlopEffect(self._pixel_buffer_list[i], color=red, slowness=speed) for i in range(4) ]
        else:
            return [ WipeFillEffect(self._pixel_buffer, color=PURPLE, slowness=1) ]




if __name__ == "__main__":

    #Note: for internal(built-in) pixels on CircuitPlayground import of cp takes care of this
    pixels = neopixel.NeoPixel(board.D2, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    #pixels = cp.pixels
    pixels.auto_write = False

    cmd = ""
    while cmd.split(' ')[0] not in ValidEffects:
        cmd = input("Effect? ")

    start_time_ns = time.monotonic_ns()

    while cmd != "Quit":

        presentation = Presentation()
        pixel_buffer = presentation.pixel_buffer()
        pixel_buffer_list = presentation.pixel_buffer_list()

        try:
            comp = cmd.split(' ')[1]
        except:
            comp = "full"

        if comp == "groups":
            presentation.sideLightGroups(12)          #  12 groups controlled with indices in range(12)
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()

            compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp == "oval":
            presentation.oval()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()
            compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp == "7segment":
            presentation.sideLight7Segment()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()
            compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp in ValidDivisions:
            try:
                num_divisions = int(comp)
            except:
                num_divisions = 2
            presentation.sideLightDivisions(num_divisions)
            compositor = presentation.compositor()
            pixel_buffer_list = presentation.pixel_buffer_list()
            compositor.compose(pixel_buffer_list, pixels)
            chooser = EffectChooser(pixel_buffer_list=pixel_buffer_list)
        else:
            presentation.sideLight()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()

            compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)


        effects = chooser.get_chosen_effects(cmd)
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
            if pixel_buffer_list is None:
                compositor.compose(pixel_buffer, pixels)
            else:
                compositor.compose(pixel_buffer_list, pixels)
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

        # prompt for another effect
        cmd = ""
        while cmd.split(' ')[0] not in ValidEffects:
            cmd = input("3ffect? ")

        # rebase start after reading, since we do not want to count that delay
        start_time_ns = time.monotonic_ns()




