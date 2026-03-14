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
    def __init__(self, pin_a_name, pin_b_name):
        """
        Initialize the neopixels and the buttons
        Initialize all of the working variables you need to track button state and current selection
        of the index.
        """
        self._bcount = 0
        self.color_capture = 0
        self.color_change = 0
        self.active_effect_index = 0
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

    def new_effect_requested(self):
        """
        Debounce this.    Use button.released for the triggering event.
        """
        self.a_button.update()
        return self.a_button.pressed

    def check_input_a(self):
        self.a_button.update()
        if self.a_button.pressed:
            print("Button A pressed")
            while self.a_button.pressed:
                time.sleep(0.01)
            print("Button A released")
            self.color_capture = 1
            return self.color_capture
            #print("log, A")

    def check_input_b(self):
        self.b_button.update()
        if self.b_button.pressed:
            print("Button B pressed")
            while self.b_button.pressed:
                time.sleep(0.01)
            print("Button B released")
            self.color_change = 1
            return self.color_change

    def chosen_color(self, active_effect_index):
        """
        Caller passes in the index of the current running effect.    This helps set up the chooser to start with the current
        effect index.    This helps when someone instructs the operator to run the effect immediately before or after, etc...
        It also permits the caller to resume the currently active effect if no change is made by just pressing
        the end-selection button.
        """

        #Flags
        self.b_count = active_effect_index
        self.color_capture = 0
        self.color_change = 0
        print("colorchoose(", active_effect_index, ") called.")

        while not check_input_a(self):
            print("log, b_count = " + str(b_count))
            self.active_effect_index = b_count
            if check_input_b(self):
                b_count = (b_count + 1) % NUM_PIXELS
            # Display the value of currently selected effect_index
            pixels.fill(ColorChooser.OFF)
            for i in range(active_effect_index+1):
                pixels[i]=ColorChooser.colors[i]
        
        return self._bcount

if __name__ == "__main__":

    # firs time, we'll just start in a random spot to help with testing
    last_choice = int(random.random() * 10)
    effect = OneColorEffect(pixels, last_choice)


    """
    This effect can be used to test the control flow when the colorchoose function DOES NOT BLOCK.
    """

    cc = ColorChooser(board.BUTTON_A, board.BUTTON_B)
    effect.reset(ColorChooser.colors[1])
    while True:
        if cc.new_effect_requested():
            color_index = cc.chosen_color()
            effect.reset(ColorChooser.colors[color_index])
        for _ in range(NUM_PIXELS * OneColorEffect.CYCLES_PER_PIXEL):
            effect.animate()
            time.sleep(0.02)
        time.sleep(0.02)


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
