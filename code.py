"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076
https://github.com/FRC1076

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
#from adafruit_circuitplayground import cp
import gc
import board
import neopixel
import random
import time
from NeoConfig import*
from PixelBuffer import PixelBuffer
from Compositor import Compositor
from Physics import Physics, Particle
from LightingEffects import RunnerEffect, FlipFlopEffect, WipeFillEffect, SqueezeFillEffect, BlinkyEffect
from LightingEffects import DripEffect, RainbowEffect, SoundMeterEffect, GradientEffect
from EffectChooser import EffectChooser


PICO_PIN = board.GP15
#KEYBOAR_PIN = board.D2
#PLAYGROUND_PIN = board.D10
NEO_PIN = PICO_PIN



# LED strings removes as duplicate in NeoConfig

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


#colors and brightness were moves out of code.py beucase they are already imported into it from the NeoConfig file.



DIGIT_ONE_ROWS = 36
DIGIT_ONE_NUM_PIXELS = 78
NUM_PIXELS = 78



def show_help():

    print("effect compositor color [speed | other options]")
    print("Example: flipflop 12 green slow")
    print("Example: drip full blue fast")

    print("\nEFFECTS")
    for effect_cmd in ValidEffects:
        print("   ", effect_cmd)

    print("\nCOMPOSITORS")
    for c in ValidCompositors:
        print("   ", c)

    print("\nCOLORS")
    for c in ValidColors.keys():
        print("   ", c)

    print("OPTIONS")
    for opt in ValidSpeeds:
        print("   ", opt)


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
        self._buffer = PixelBuffer(NUM_PIXELS)
        self._compositor.passThru(NUM_PIXELS)

    def sideLightGroups(self, num_groups=2):
        """
        This should work cleanly with 2, 3, 5, 4, 6 and their products.
        """
        self._buffer = PixelBuffer(num_groups)
        self._compositor.groupsOfN(NUM_PIXELS, num_groups)


    def sideLightDivisions(self, num_divisions=2):
        """
        This should work cleanly with 2, 3, 5, 4, 6 and their products.
        """
        #self._buffer_list = [ PixelBuffer(SIDELIGHT_PIXELS // num_divisions) for i in range(num_divisions) ]
        # Note: compositor creates the buffers
        self._compositor.divisionsOfN(NUM_PIXELS, num_divisions)

    def sideLight7Segment(self):
        groups = 24
        self._buffer = PixelBuffer(groups)
        self._compositor.eightHorizontal(groups)

    def oval(self):
        groups = NUM_PIXELS // 2
        self._buffer = PixelBuffer(groups)
        self._compositor.oval(NUM_PIXELS, groups)

    def digitOneH(self):
        self._buffer = PixelBuffer(DIGIT_ONE_ROWS)
        self._compositor.digitOneHSlices(DIGIT_ONE_ROWS)

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
        self._cmds =   [ "runner digit1H red fast" ]
        self._ndx = 0
        self._interval_timer = None

    def nextCommand(self):

        cmd = None
        gc.collect()
        print("Memory free:", gc.mem_free())

        # first time
        #if self._interval_timer == None or ((time.monotonic_ns() - self._interval_timer) > SyntheticDemoer.INTERVAL_NS):
        #    self._interval_timer = time.monotonic_ns()

        cmd = self._cmds[self._ndx]
        self._ndx += 1 % len(self._cmds)    # wrap!

        return cmd








if __name__ == "__main__":

    demoer = None
    #demoer = SyntheticDemoer()      # comment this out to accept commands from the console

    #Note: for internal(built-in) pixels on CircuitPlayground import of cp takes care of this
    pixels = neopixel.NeoPixel(NEO_PIN, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    #pixels = cp.pixels
    pixels.auto_write = False

    cmd = ""
    while cmd.split(' ')[0] not in ValidEffects:
        if not demoer is None:
            cmd = demoer.nextCommand()
        else:
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
        elif comp == "digit1H":
            presentation.digitOneH()
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




