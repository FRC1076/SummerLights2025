"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076
https://github.com/FRC1076
"""
import gc
import board
import neopixel
import random
import time
from Compositor import Compositor
from HardwareAwareness import HardwareAwareness
from PixelBuffer import PixelBuffer
from ButtonChooser import ColorChooser
from ControlEffects import WaitEffect
from BreathingEffect import BreathingEffect
from EffectChooser import EffectChooser
from DemoCommands import ValidEffects, ValidDivisions



#NEO_PIN = PICO_PIN

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
FULL_RED = (255, 0, 0)
TIMED = (1, 1, 1)



class Presentation:
    """
    A presentation is a collection and configuration of the components necessary to animate,
    render, arrange, and present a responsive lighting effect.
    They include neopixel choice
    """
    def __init__(self, my_digit_index, my_num_pixels):
        self._compositor = Compositor()
        self._buffer_list = None
        self._buffer = None
        self._my_digit_index = my_digit_index       #  This is different for each digit
        self._my_num_pixels = my_num_pixels

    def drippingFeatherSeparate(self):
        pixel_buffer = PixelBuffer(FEATHER_WING_COLUMNS)
        self._buffer_list = [ pixel_buffer ] * FEATHER_WING_ROWS
        #for i in range(FEATHER_WING_ROWS):
        #self._buffer_list[i] = PixelBuffer(FEATHER_WING_COLUMNS)
        self._compositor.bufferList(list_of_buffers=self._buffer_list)

    def playgroundBuiltIn(self):
        self._buffer = PixelBuffer(CP_PIXELS)
        self._compositor.passThru(CP_PIXELS)

    def sideLight(self):
        self._buffer = PixelBuffer(self._my_num_pixels)
        self._compositor.passThru(self._my_num_pixels)

    def sideLightGroups(self, num_groups=2):
        """
        This should work cleanly with 2, 3, 4, 5, 6 and their products.
        """
        self._buffer = PixelBuffer(num_groups)
        self._compositor.groupsOfN(self._my_num_pixels, num_groups)

    def sideLightDivisions(self, num_divisions=2):
        """
        This should work cleanly with 2, 3, 5, 4, 6 and their products.
        """
        #self._buffer_list = [ PixelBuffer(SIDELIGHT_PIXELS // num_divisions) for i in range(num_divisions) ]
        # Note: compositor creates the buffers
        self._compositor.divisionsOfN(self._my_num_pixels, num_divisions)

    def sideLight7Segment(self):
        groups = 24
        self._buffer = PixelBuffer(groups)
        self._compositor.eightHorizontal(groups)

    def oval(self):
        groups = NUM_PIXELS // 2
        self._buffer = PixelBuffer(groups)
        self._compositor.oval(NUM_PIXELS, groups)

    """
    The topology oriented compositors pick from a list of the digit compositors
    based on the known digit index.    Each digit has a unique HSlice, VSlice, and Stroke compositor.
    Pick the appropriate compositor based on the index.
    Call the creation function to build the compositor.
    Use the returned value to allocate the correctly sized PixelBuffer
    """
    def digitCompositor(self, comp_functions):
        my_comp_function = comp_functions[self._my_digit_index]
        num_pixels = my_comp_function()
        self._buffer = PixelBuffer(num_pixels)

    def digitH(self):
        c = self._compositor
        self.digitCompositor([ c.digit1HSlices, c.digit0HSlices, c.digit7HSlices, c.digit6HSlices ])

    def digitV(self):
        c = self._compositor
        self.digitCompositor([ c.digit1VSlices, c.digit0VSlices, c.digit7VSlices, c.digit6VSlices ])

    def digitS(self):
        c = self._compositor
        self.digitCompositor([ c.digit1Strokes, c.digit0Strokes, c.digit7Strokes, c.digit6Strokes ])

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


class SyntheticDemoer:

    NANO_SECONDS_PER_SECOND = 1000000000
    INTERVAL_SECS = 10
    INTERVAL_NS = NANO_SECONDS_PER_SECOND*INTERVAL_SECS

    def __init__(self):
        self._shows =   [( "breathing full digitH purple fast", ),
                        ( "runner 12 digitV purple medium", ),
                        ( "Wait digitH red fast", "wipe digitH red medium",
                          "Wait digitV red fast", "wipe digitV red medium",
                          "Wait digitS red fast", "wipe digitS red medium", ),
                        ( "Wait digitH blue fast", "wipe digitH blue medium",
                          "Wait digitV blue fast", "wipe digitV blue medium",
                          "Wait digitS blue fast", "wipe digitS blue medium", ),
                        ( "flipflop 4 digitV red slow", ),
                        ( "flipflop 4 digitV blue slow", ),
                        ( "flashing digitH purple medium", ),
                        ( "gradient digitS red medium", ), # actually shows rainbow
                        ( "multicolor digitS purple fast", ),
                        ( "clear all", ),
                       ]

        self._show_ndx = None
        self._previous_show_ndx = 0       # this kicks starts the first choice
        self._cmd_ndx = 0
        self._interval_timer = None
        try:
            self._pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=True)
        except ValueError as ve:
            print("Unable to initialize onboard neopixels:", str(ve))
            print("Trying to free up the resource")
            try:
                import adafruit_circuitplayground as cp
                cp.cp.pixels.deinit()
                self._pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1, auto_write=True)
            except NameError as ne:
                print("Unable to get a reference to free up the resource:", str(ne))
                print("NeoPixels will likely not work.")
            else:
                print("Onboard NeoPixels initialized successfully!")
        else:
            print("Onboard NeoPixels initialized successfully!")

        self._button_chooser = ColorChooser(self._pixels, board.BUTTON_A, board.BUTTON_B)
        print("Choose commands using the built-in A and B buttons")

    def needsControl(self):
        needs = self._button_chooser.new_effect_requested()
        if needs:
            # Let the demoer know that it is time for a new show!
            self._show_ndx = None
        return needs

    def nextCommand(self):
        #
        if self._show_ndx == None:
            """
            Take a break for user interaction, a little delay is fine for some gc
            Recent reports are 78096 bytes free on the CircuitPlayground Bluefruit
            """
            gc.collect()
            print("Memory free:", gc.mem_free())
            self._show_ndx = self._button_chooser.chosen_color(self._previous_show_ndx)
            self._previous_show_ndx = self._show_ndx     # record for next time
            self._cmds = self._shows[self._show_ndx]
            self._cmd_ndx = 0

        cmd = self._cmds[self._cmd_ndx]
        self._cmd_ndx = (self._cmd_ndx + 1) % len(self._cmds)    # wrap!
        if cmd == "Repeat":     # go to beginning skipping the Repeat directive
            cmd = self._cmds[self._ndx]
            self._ndx = (self._ndx + 1) % len(self._cmds)   # wrap!

        return cmd


if __name__ == "__main__":

    hdw = HardwareAwareness()
    #Note: for internal(built-in) pixels on CircuitPlayground import of cp takes care of this
    pixels = hdw.getPixels()
    print("Hardware allocated:", len(pixels), "NeoPixels at brightness:", pixels.brightness)

    if hdw.getEnvironment() in ["demo", "wokwi", "standalone"]:
        demoer = None
    else:
        demoer = SyntheticDemoer()      # uses ColorChooser to choose the effect

    pixels.auto_write = False

    cmd = ""
    while cmd.split(' ')[0] not in ValidEffects:
        if not demoer is None:
            cmd = demoer.nextCommand()
        else:
            cmd = input("Effect? ")

    start_time_ns = time.monotonic_ns()

    while cmd != "Quit":

        presentation = Presentation(hdw.getIndex(), hdw.getNumPixels())
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

            #compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp == "oval":
            presentation.oval()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()
            #compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp == "digitH":
            presentation.digitH()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()
            #compositor.compose(pixel_buffer, pixels)    MCJXXX
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp == "digitV":
            presentation.digitV()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()
            #compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp == "digitS":
            presentation.digitS()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()
            #compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp == "7segment":
            presentation.sideLight7Segment()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()
            #compositor.compose(pixel_buffer, pixels)
            chooser = EffectChooser(pixel_buffer=pixel_buffer)
        elif comp in ValidDivisions:
            try:
                num_divisions = int(comp)
            except:
                num_divisions = 2
            presentation.sideLightDivisions(num_divisions)
            compositor = presentation.compositor()
            pixel_buffer_list = presentation.pixel_buffer_list()
            #compositor.compose(pixel_buffer_list, pixels)
            chooser = EffectChooser(pixel_buffer_list=pixel_buffer_list)
        else:
            presentation.sideLight()
            compositor = presentation.compositor()
            pixel_buffer = presentation.pixel_buffer()

            #compositor.compose(pixel_buffer, pixels)
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
        while (len(do_effects) > 0 or len(next_do_effects) > 0) and (demoer is None or not demoer.needsControl()):

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
            elif adjust > 40:
                print("WARNING: Slip of  ", adjust-20, "milliseconds")

            # rebase start after sleep, since we do not want to count that
            start_time_ns = time.monotonic_ns()

        # prompt for another effect
        cmd = ""
        while cmd.split(' ')[0] not in ValidEffects:
            if not demoer is None:
                cmd = demoer.nextCommand()
            else:
                cmd = input("3ffect? ")

        # rebase start after reading, since we do not want to count that delay
        start_time_ns = time.monotonic_ns()

