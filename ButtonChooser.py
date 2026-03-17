"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
https://github.com/FRC1076
"""
from adafruit_debouncer import Button
import adafruit_circuitplayground as cp
import time
import board
import neopixel
import random
import digitalio

class OneColorEffect:

    CYCLES_PER_PIXEL = 5

    def __init__(self, pixels, color):
        self._pixels = pixels
        self.reset(color)

    def set_color(self, color):
        self._color = color

    def reset(self, color):
        self._color = color
        self._cycle = 0
        self._ndx = 0
        
    def dump(self):
        print("Index:", self._ndx, "Cycle:", self._cycle, "Color:", self._color)

    def animate(self):
        """
        Light a pixel on the beginning of the cycle
        Clear everything when wrapping around
        """
        if self._ndx == 0:
            pixels.fill(ColorChooser.OFF)
        if self._cycle == 0:
            pixels[self._ndx] = self._color
            self._ndx = (self._ndx + 1) % len(self._pixels)

        self._cycle = (self._cycle + 1) % OneColorEffect.CYCLES_PER_PIXEL



class ColorChooser():
    #Constants
    OFF = (0, 0, 0)
    RED = (64, 0, 0)
    ORANGE = (64, 32, 0)
    YELLOW = (64, 64, 0)
    GREEN = (0, 64, 0)
    CYAN = (0, 64, 64)
    BLUE = (0, 0, 64)
    PURPLE = (32, 0, 32)
    WHITE = (64, 64, 64)
    BROWN = (48, 12, 12)
    PINK = (64, 21, 46)
    colors = [ RED, WHITE, YELLOW, BROWN, CYAN, BLUE, PURPLE, ORANGE, GREEN, PINK]

    """
        cc = ColorChooser()

        while running_FATAL_effects:
            if cc.new_effect_requested():
                new_effect_index = cc.chosen_color(active_effect_index)
            if new_effect_index != active_effect_index:
                active_effect_index = new_effect_index

            reinitialize_effects_with_index(active_effect_index)
    """
    def __init__(self, pixels, pin_a_name, pin_b_name):
        """
        Initialize the neopixels and the buttons
        Initialize all of the working variables you need to track button state and current selection
        of the index.
        """
        self.pixels = pixels
        self.bcount = 0
        # initialize a button
        a_pin = digitalio.DigitalInOut(pin_a_name)
        a_pin.direction = digitalio.Direction.INPUT
        # CircuitPlayground buttons connect to the 5v rail,
        # so they require a pulldown resister.
        a_pin.pull = digitalio.Pull.DOWN
        # you can find the source code for the Button()
        # https://github.com/adafruit/Adafruit_CircuitPython_Debouncer/blob/main/adafruit_debouncer
        # Built-in buttons return True when pressed.
        self.a_button = Button(a_pin, value_when_pressed=True)

        b_pin = digitalio.DigitalInOut(board.BUTTON_B)
        b_pin.direction = digitalio.Direction.INPUT
        b_pin.pull = digitalio.Pull.DOWN
        self.b_button = Button(b_pin, value_when_pressed=True)
        
    def deinit(self):
        try:
            self.pixels.deinit()
            self.a_button.deinit()
            self.b_button.deinit()
        except:
            pass

    def new_effect_requested(self):
        """
        Debounce this.    Use button.released for the triggering event.
        """
        return self.button_a_released()
        
    def button_a_released(self):
        self.a_button.update()
        return self.a_button.released
        
    def chosen_color(self, active_effect_index):
        """
        Caller passes in the index of the current running effect.    This helps set up the chooser to start with the current
        effect index.    This helps when someone instructs the operator to run the effect immediately before or after, etc...
        It also permits the caller to resume the currently active effect if no change is made by just pressing
        the end-selection button.
        """
        self.b_count = active_effect_index         # start at the setting provided
        update_pixels = True         # use this to force an update to the pixel ring
        while not self.button_a_released():

            self.b_button.update()
            if self.b_button.released:
                #  Update the index, and only update the pixels if something changes
                self.b_count = (self.b_count + 1) % len(self.pixels)
                update_pixels = True
                
            if update_pixels:
                self.pixels.fill(ColorChooser.OFF)
                for i in range(self.b_count+1):
                    self.pixels[i]=ColorChooser.colors[i]
                update_pixels = False      #  clear the display triggering
            time.sleep(0.02)
        
        return self.b_count


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
    
