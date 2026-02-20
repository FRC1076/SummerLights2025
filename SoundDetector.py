"""
   Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
   https://github.com/FRC1076 

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import time
import array
import math
import audiobusio
import board
import neopixel
import digitalio
# We want to do our own thing with this.   Maybe it later
#from adafruit_circuitplayground import cp

class SoundDetector:

    MAGNITUDE_SCALE = 0.1
    PIXEL_SCALE = 120

    Mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)

    def __init__(self):
        self._mic = SoundDetector.Mic
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

    def getLevelPct(self):
        """
        Get the magnitude from the mic and convert it and return as pixel scale
        """
        self._mic.record(self._samples, len(self._samples))
        magnitude = SoundDetector.normalized_rms(self._samples)
        PixelPct = magnitude*SoundDetector.MAGNITUDE_SCALE / SoundDetector.PIXEL_SCALE
        if PixelPct > 1.0:
            PixelPct = 1.0
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
        PixelPct = sd.getLevelPct()
        PixelScale = int(PixelPct * len(pixels))
        print(PixelScale)

        pixels.fill((0,0,0))
        pixels.show()
        for p in range(PixelScale):
            pixels[p] = PURPLE
        pixels.show()
        time.sleep(0.1)
