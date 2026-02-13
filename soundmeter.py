import time
import array
import math
import audiobusio
import board
import neopixel
import digitalio
#import circuitplayground as cp


# Remove DC bias before computing RMS.
def mean(values):
    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))

FEATHER_WING_PIXELS = 32
NEON_PIXELS = 32
SIDELIGHT_PIXELS = 120

NUM_PIXELS = SIDELIGHT_PIXELS
COLOR_INC = 255 / NUM_PIXELS
BRIGHTNESS = 0.1
MAGNITUDE_SCALE = 0.1
LIFETIME = 10

#pixelpin = digitalio.DigitalInOut(board.GP6)
#pixelpin.direction = digitalio.Direction.OUTPUT

OFF = (0, 0, 0)
PURPLE = (92, 50, 168)
ORANGE = (235, 122, 52)
BLUE = (24, 30, 214)



class InstantFillBackground:

    def __init__(self, pixels, pixel_range=range(NUM_PIXELS), color=PURPLE, brightness=BRIGHTNESS, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done all in one shot, suitable for use as a background for some other effect.
        """
        self._pixels = pixels
        self._pixel_range = pixel_range
        self._color = color
        self._brightness = brightness
        self._maximum = 0
        self._maxlifetime = 0


        if clear_on_init:
            """
            But, do not display, just zero out everything
            """
            pixels.fill(OFF)

    def run(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        for p in self._pixel_range:
            self._pixels[p] = self._color

    def fillNshow(self,NumPixels):
        if NumPixels > self._maximum:
            self._maximum = NumPixels-1
            self._maxlifetime = LIFETIME
        else:
            if self._maxlifetime == 0:
                self._pixels[self._maximum] = OFF
                self._maximum = 0
            else:
                self._maxlifetime-=1

       # self._pixels.fill(OFF)
        for p in range(self._maximum):
            self._pixels[p] = OFF
        for p in range(NumPixels):
            self._pixels[p] = self._color

        self._pixels.show()






if __name__ == "__main__":

    mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
    samples = array.array('H', [0] * 160)
    pixels = neopixel.NeoPixel(board.D10, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    pixels.fill((0,0,0))

    purple_background_effect = InstantFillBackground(pixels)
    pixels.show()

    while True:
        mic.record(samples, len(samples))
        magnitude = normalized_rms(samples)
        PixelScale = int(magnitude*MAGNITUDE_SCALE)
        if PixelScale >= NUM_PIXELS:
            PixelScale = NUM_PIXELS
        print((magnitude, PixelScale,))
        purple_background_effect.fillNshow(PixelScale)
        time.sleep(0.1)



    """
    One time setup with solid PURPLE

    print("Display background once")
    purple_background_effect = InstantFillBackground(pixels)
    purple_background_effect.run()
    pixels.show()
    time.sleep(3)


    Pause for dramatic effect... ;)
    Create the generator that does the steps for the effect
    These generators need to be recreated in order to repeat
    (unless they have the repeat built-in)

    wipe_orange = orange_background_wipe.runner()
    blue_car_drive_forward = blue_car.runner(slowness=4)

    print("Display the color wipe")
    for _ in wipe_orange:
        pixels.show()
        time.sleep(0.020)

    for _ in blue_car_drive_forward:
        pixels.show()
        time.sleep(0.020)
    """


