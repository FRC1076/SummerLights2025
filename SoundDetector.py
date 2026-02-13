import time
import array
import math
import audiobusio
import board
import neopixel
import digitalio
#import circuitplayground as cp

class SoundDetector:

    MAGNITUDE_SCALE = 0.1
    PIXEL_SCALE = 120

    def __init__(self):
        self._mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
        self._samples = array.array('H', [0] * 160)

    # Remove DC bias before computing RMS.
    def mean(values):
        return sum(values) / len(values)

    def normalized_rms(values):
        minbuf = int(SoundDetector.mean(values))
        samples_sum = sum(
            float(sample - minbuf) * (sample - minbuf)
            for sample in values
        )

        return math.sqrt(samples_sum / len(values))

    def getLevel(self):
        """
        Get the magnitude from the mic and convert it and return as pixel scale
        """
        self._mic.record(self._samples, len(self._samples))
        magnitude = SoundDetector.normalized_rms(self._samples)
        PixelPct = magnitude*SoundDetector.MAGNITUDE_SCALE / SoundDetector.PIXEL_SCALE
        return PixelPct

if __name__ == "__main__":

    NUM_PIXELS = 120
    BOARD_PIN = board.D10
    BRIGHTNESS = 0.3
    PURPLE = (253, 0, 250)
    sd = SoundDetector()
    pixels = neopixel.NeoPixel(BOARD_PIN, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    pixels.fill((0,0,0))
    pixels.show()

    while True:
        PixelPct = sd.getLevel()
        if PixelPct >= 1.0:
            PixelPct = 1.0
        PixelScale = int(PixelPct * len(pixels))
        print(PixelScale)

        pixels.fill((0,0,0))
        pixels.show()
        for p in range(PixelScale):
            pixels[p] = PURPLE
        pixels.show()
        time.sleep(0.1)
