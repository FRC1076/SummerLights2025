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

    MAGNITUDE_SCALE = 0.01

    def __init__(self, pixel_scale=78):
        try:
            self._mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
        except ValueError as ve:
            print("Problem: ", str(ve), "while trying to initialize the microphone")
            print("Cleaning up and trying again")
            from adafruit_circuitplayground import cp
            # Release the pins held by the high-level library
            if hasattr(cp, '_mic'):
                cp._mic.deinit()
            elif hasattr(cp, '_microphone'):
                cp._microphone.deinit()
            print("Cleaned up!")

            # try again without trying
            self._mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
        self._samples = array.array('H', [0] * 160)
        self._cycle = 0
        self._pixel_scale = pixel_scale

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
        # Log magnitude every 100 cycles to cut down on logging
        self._cycle = (self._cycle + 1) % 100
        if self._cycle == 0:
            print("Magnitude:", magnitude, "Samples:", self._samples)
        PixelPct = magnitude*SoundDetector.MAGNITUDE_SCALE / self._pixel_scale
        if PixelPct > 1.0:
            PixelPct = 1.0
        return PixelPct

if __name__ == "__main__":

    NUM_PIXELS = 60
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
        #print(PixelScale)

        pixels.fill((0,0,0))
        pixels.show()
        for p in range(PixelScale):
            pixels[p] = PURPLE
        pixels.show()
        time.sleep(0.02)
