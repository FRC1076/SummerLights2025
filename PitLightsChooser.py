"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
https://github.com/FRC1076
"""
import time
import board
import neopixel
import random
import rotaryio
import digitalio
from adafruit_debouncer import Debouncer

FEATHER_COLUMNS = 4
FEATHER_ROWS = 8
NUM_PIXELS = FEATHER_ROWS*FEATHER_COLUMNS
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
LT_GREEN = (0, 50, 0)
MED_GREEN = (0, 150, 0)

def signum(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0

class PushButton:

    def __init__(self, button_pin):
        self._button = digitalio.DigitalInOut(button_pin)
        self._button.direction = digitalio.Direction.INPUT
        self._button.pull = digitalio.Pull.UP
        self._debouncer = Debouncer(self._button)
    
    def pressed(self):
        """
        Button is connected to ground, so when it is pressed, the value on the pin
        is 0, which equates to False
        """
        return self._debouncer.fell

    def released(self):
        return self._debouncer.rose

    def update(self):
        self._debouncer.update()

class RotarySelector:

    def __init__(self, pinA, pinB, button_pin, num_selections, name="Vert", sense=1):
        self._encoder = rotaryio.IncrementalEncoder(pinA, pinB)
        self._button = PushButton(button_pin)
        self._num_selections = num_selections
        self._last_selection = None
        self._selection = None
        self._button_down = False
        self._sense = sense
        self._name = name

    def selection(self):
        """
        Cover the first use and rollover.  Return the current selection.
        """
        self._selection = self._encoder.position
        if self._last_selection is None or self._selection != self._last_selection:
            if self._last_selection is None:
                self._selection = 0
            else:
                self._selection = ((self._selection + self._sense*signum(self._last_selection-self._selection)) % self._num_selections)         
        self._last_selection = self._selection
        return self._selection

    def button_pressed(self):
        return self._button.pressed()




def rowcol_to_index(rows, columns, position):
    """
    If column is even, then mapping is easy
    """
    if position[1] % 2 == 0:
        ndx = position[1]*rows + position[0]
    else:
        ndx = position[1]*rows + rows - position[0] - 1
    return ndx


CURSOR_COLOR = (0, 0, 100)
ACTIVE_PIXEL_COLOR = (0, 100, 0)
INACTIVE_PIXEL_COLOR = (100, 0, 0)
OFF = (0, 0, 0)

class Cursor:
    """
    Keep track of where the cursor is and move it around accordingly.
    Be sure to restore the underlying pixel when moving away
    """

    def __init__(self, pixels, rows=FEATHER_ROWS, columns=FEATHER_COLUMNS):
        self._pixels = pixels
        self._rows = rows
        self._columns = columns
        self._position = (0,0)
        self._under_pixel = INACTIVE_PIXEL_COLOR
        self._under_pixel_index = 0
        self._index = 0
        self.move_to(self._position)

    def display(self):
        """
        Save the underpixel state
        """
        pixels.show()

    def move_to(self, position):
        """
        Restore the underpixel and to the new position
        """
        pixels[self._under_pixel_index] = self._under_pixel
        self._index = rowcol_to_index(self._rows, self._columns, position)
        self._under_pixel_index = self._index
        self._under_pixel = pixels[self._index]
        pixels[self._index] = CURSOR_COLOR

    def toggle(self):
        print("Toggle")
        if self._under_pixel == ACTIVE_PIXEL_COLOR:
            self._under_pixel = INACTIVE_PIXEL_COLOR
        elif self._under_pixel == INACTIVE_PIXEL_COLOR:
            self._under_pixel = ACTIVE_PIXEL_COLOR


chooser = RotarySelector(board.GP18, board.GP19, board.GP12, 2, name="Vert", sense=1)
horiz = RotarySelector(board.GP16, board.GP17, board.GP13, FEATHER_COLUMNS, name="Horiz", sense=1)
pixels = neopixel.NeoPixel(board.GP15, NUM_PIXELS, brightness=1.0, auto_write=False)
pixels.fill(INACTIVE_PIXEL_COLOR)
cursor = Cursor(pixels)

def display_glyph(pixels, glyph, color=PURPLE):
    for pos in glyph:
        ndx = rowcol_to_index(FEATHER_ROWS, FEATHER_COLUMNS, pos)
        pixels[ndx]=color


def translate(glyph, displacement):
    return [ (r+displacement[0],c+displacement[1]) for (r,c) in glyph ]

purple_glyph = [ (1, 1), (1, 2), (2, 1), (2, 2) ]
white_glyph = translate(purple_glyph, (4,0))
purple_aura = [ (0,0), (0,1), (0,2), (0,3),
                (1,3),               (2,3),
                (3,3),               (3,2),
                (3,1), (3,0), (2,0), (1,0) ]
white_aura = translate(purple_aura, (4,0))

def display_glyph(pixels, glyph, color=PURPLE):
    for pos in glyph:
        ndx = rowcol_to_index(FEATHER_ROWS, FEATHER_COLUMNS, pos)
        print("pixels at", ndx, "=", color)
        pixels[ndx]=color

class Aura:
    def __init__(self, pixels, glyph, colorA, colorB):
        self._pixels = pixels
        self._glyph = glyph
        self._colorA = colorA
        self._colorB = colorB
        self._state = None
        self._frame_index = 0

    def select(self):
        self._state = self._colorA
        self._frame_index = 0

    def animate(self):
        pixel_index = rowcol_to_index(FEATHER_ROWS, FEATHER_COLUMNS, self._glyph[self._frame_index])
        self._pixels[pixel_index] = self._state
        self._frame_index = (self._frame_index + 1) % len(self._glyph)
        if self._frame_index == 0:     # just wrapped, time to swap
            if self._state == self._colorA:
                self._state = self._colorB
            else:
                self._state = self._colorA

    def deselect(self):
        pixel_index = rowcol_to_index(FEATHER_ROWS, FEATHER_COLUMNS, self._glyph[self._frame_index])
        self._pixels[pixel_index] = OFF
        self._frame_index = (self._frame_index + 1) % len(self._glyph)
        if self._frame_index == 0:
            self._state = None       

#for c in range(FEATHER_COLUMNS):
#    for r in range(FEATHER_ROWS):
#        print((r,c), "=>", rowcol_to_index(FEATHER_ROWS, FEATHER_COLUMNS, (r,c)))

display_glyph(pixels, purple_glyph, PURPLE)
display_glyph(pixels, white_glyph, WHITE)

auras = [ None ] * 2
auras[0] = Aura(pixels, purple_aura, LT_GREEN, MED_GREEN)
auras[1] = Aura(pixels, white_aura, LT_GREEN, MED_GREEN)

last_choice = None

while True:
    choice = 1     # either 0 or 1

    if random.random() > 0.88:
        if choice == 0:
            choice = 1
        else:
            choice = 0

    if choice != last_choice:
        try:
            aura[last_choice].deselect()
        except:
            pass
        auras[choice].select()

    auras[choice].animate()

    pixels.show()

    if chooser.button_pressed():
        time.sleep(0.1)
        while not chooser.button_released():
            time.sleep(0.1)
        print("Activated selection:", choice)

    last_choice = choice
    time.sleep(0.02)
