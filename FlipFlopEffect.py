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
from NeoConfig import OFF, PURPLE, BRIGHTNESS

class FlipFlopEffect:
    """
    Alternate between half on and half off on the domain
    """
    def __init__(self, pixel_buffer, color=PURPLE, slowness=100, brightness=BRIGHTNESS, name="FlipFlop"):
        """
        Base class for lighting effects
        Could be useful for documentation, or maybe actually used as a base class
        Note, this relies on constants from elsewhere.    Should probably import them instead of assuming
        they have been imported.
        """
        self._pixel_buffer = pixel_buffer
        self._color = color
        self._slowness = slowness
        self._brightness = brightness
        self._name=name

    def make_generator(self):
        """
        Make flip and flop over half of the domain at a time
        """
        plen = len(self._pixel_buffer)
        half_len = plen // 2
        while True:
            for p in range(half_len):
                self._pixel_buffer[p] = self._color

            for p in range(half_len, plen):
                self._pixel_buffer[p] = OFF

            for _ in range(self._slowness):
                yield

            for p in range(half_len):
                self._pixel_buffer[p] = OFF

            for p in range(half_len, plen):
                self._pixel_buffer[p] = self._color

            for _ in range(self._slowness):
                yield

