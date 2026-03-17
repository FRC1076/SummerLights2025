"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
https://github.com/FRC1076
"""
import board
import neopixel
import random
import time

from ButtonChooser import ColorChooser, OneColorEffect

if __name__ == "__main__":

    #
    #   If the circuitplayground library has been initialized elsewhere, the internal NEOPIXEL pin will
    #   be claimed.   We have to free it up before we can control it our own way.
    #
    NUM_PIXELS=10
    try:
        pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=True)
    except ValueError as ve:
        print("Unable to initialize neopixels:", str(ve))
        print("Trying to free up the resource")
        try:
            import adafruit_circuitplayground as cp
            cp.cp.pixels.deinit()
            pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=True)
        except NameError as ne:
            print("Unable to get a reference to free up the resource:", str(ne))
            print("Things likely will not work...")
        else:
            print("Neopixels initialized successfully!")
    else:
        print("Neopixels initialized successfully!")

    # for the first time, we'll pretend it has been running for some time
    previous_index = int(random.random() * NUM_PIXELS) % NUM_PIXELS
    effect = OneColorEffect(pixels, ColorChooser.colors[previous_index])

    """
    This effect can be used to test the control flow to make sure the colorchoose
    function DOES NOT BLOCK unless the REQUEST button is released.
    """
    cc = ColorChooser(pixels, board.BUTTON_A, board.BUTTON_B)
    
    while True:
        """
        The effect always runs in this main loop, only ever interrupted by the chooser request
        """
        if cc.new_effect_requested():
            chosen_index = cc.chosen_color(previous_index)
            if previous_index != chosen_index:
                print("Chose: ", chosen_index)
                effect.reset(ColorChooser.colors[chosen_index])
                previous_index = chosen_index
            else:
                print("Unchanged")
        effect.animate()
        time.sleep(0.02)
    
    
    # Always try to cleanup, although this is not reachable
    self.deinit()
 
