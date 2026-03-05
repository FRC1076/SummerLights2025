"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
https://github.com/FRC1076
"""
from adafruit_debouncer import Button
import time
import board
import neopixel
import random
import digitalio


NUM_PIXELS=10

#
#   If the circuitplayground library has been initialized, the internal NEOPIXEL pin will
#   be claimed.   We have to free it up before we can control it our own way.
#
try:
    pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=True)
except ValueError:
    cp.pixels.deinit()
    pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=True)


a_pin = digitalio.DigitalInOut(board.BUTTON_A)
a_pin.direction = digitalio.Direction.INPUT
# CircuitPlayground buttons connect to the 5v rail,
# so they require a pulldown resister.
a_pin.pull = digitalio.Pull.DOWN
# you can find the source code for the Button()
# https://github.com/adafruit/Adafruit_CircuitPython_Debouncer/blob/main/adafruit_debouncer
# Built-in buttons return True when pressed.
a_button = Button(a_pin, value_when_pressed=True)

b_pin = digitalio.DigitalInOut(board.BUTTON_B)
b_pin.direction = digitalio.Direction.INPUT
b_pin.pull = digitalio.Pull.DOWN
b_button = Button(b_pin, value_when_pressed=True)

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

    def animate(self):
        """
        Light a pixel on the beginning of the cycle
        """
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
    def __init__(self):
        """
        Initialize the neopixels and the buttons
        Initialize all of the working variables you need to track button state and current selection
        of the index.
        """
        self._bcount = 0
        pass

    def new_effect_requested(self):
        """
        Debounce this.    Use button.released for the triggering event.
        """
        pass

    def chosen_color(self, active_effect_index):
        """
        Caller passes in the index of the current running effect.    This helps set up the chooser to start with the current
        effect index.    This helps when someone instructs the operator to run the effect immediately before or after, etc...
        It also permits the caller to resume the currently active effect if no change is made by just pressing
        the end-selection button.
        """
        return self._bcount




def colorchoose(effect_index):

    #Flags
    b_count = effect_index
    color_capture = 0
    color_change = 0
    print("colorchoose(", effect_index, ") called.")
    

    while True:
        color_capture = 0
        color_change = 0

        while color_capture == 0 and color_change == 0:
            # The sense of the debouncer is backwards
            # It reports press on release, and release on press
            # I think this is because the button is configured for PULL down
            # Perhaps there is an option to the debouncer to reverse the sense?
            # call update() regularly so the debouncer and pressed timers can be updated
            a_button.update()
            if a_button.pressed:
                print("Button A pressed")
            if a_button.released:
                print("Button A released")
                color_capture = 1
                #print("log, A")

            # call update() regularly so the debouncer and pressed timers can be updated
            b_button.update()
            if b_button.pressed:
                print("Button B pressed")
            if b_button.released:
                print("Button B released")
                color_change = 1
                #print("log, B")

            if color_change:
                print("log, b_count = " + str(b_count))
                effect_index = b_count
                b_count = (b_count + 1) % NUM_PIXELS
                # Display the value of currently selected effect_index
                pixels.fill(ColorChooser.OFF)
                for i in range(effect_index+1):
                    pixels[i]=ColorChooser.colors[i]
                # this could wrap
                #while not start_button.value:
                #pass

            if color_capture:
                return effect_index

            #pixels.show() experiment with the auto_write set to True
            time.sleep(0.02)


if __name__ == "__main__":

    # firs time, we'll just start in a random spot to help with testing
    last_choice = int(random.random() * 10)
    effect = OneColorEffect(pixels, last_choice)
   
    """
    This effect can be used to test the control flow when the colorchoose function DOES NOT BLOCK.
    
    for color_index in range(len(ColorChooser.colors)):
        effect.reset(ColorChooser.colors[color_index])
        for _ in range(NUM_PIXELS * OneColorEffect.CYCLES_PER_PIXEL):
            effect.animate()
            time.sleep(0.02)
    """
         
    NUM_TESTS = 10
    for _ in range(NUM_TESTS):
        """
        Note: colorchoose blocks execution
        The main loop of our effects has to run every 20 milliseconds
        unless it is interrupted.   We don't want to interrupt it each
        cycle.
        """
        choice = colorchoose(last_choice)
        print("Pikachu, I choose:", choice)
        last_choice = choice


    # Always try to cleanup
    try:
        pixels.deinit()
        a_button.deinit()
        b_button.deinit()
    except:
        pass
