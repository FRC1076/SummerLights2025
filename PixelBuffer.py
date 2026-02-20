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
class PixelBuffer:
    OUT_OF_RANGE_BLACK = (0,0,0)

    def __init__(self, num_pixels):
        # Store the underlying data in an internal list
        self.pixels = [ PixelBuffer.OUT_OF_RANGE_BLACK ] * num_pixels

    def __getitem__(self, index):
        """
        Use internal list for access.
        Return special black for IndexError
        """
        try:
            item = self.pixels[index]
        except IndexError:
            item = PixelBuffer.OUT_OF_RANGE_BLACK
        return item

    def __setitem__(self, index, value):
        """
        Do nothing if index is out of range
        """
        try:
            self.pixels[index] = value
        except IndexError:
            pass

    def __len__(self):
        """
        Be like a proper list and have a length
        """
        return len(self.pixels)

    def fill(self, value):
        for i in range(len(self)):
            self.pixels[i] = value


if __name__ == "__main__":

    # --- Usage ---
    # Create an instance with some data
    pixbuff = PixelBuffer(4)
    pixbuff[0] = 'red'
    pixbuff[1] = 'green'
    pixbuff[2] = 'blue'
    pixbuff[3] = 'orange'

    # Access elements using index notation
    print(f"Item at index 0: {pixbuff[0]}")
    print(f"Item at index 2: {pixbuff[2]}")
    print(f"Items using slicing: {pixbuff[1:3]}")
    print(f"Out of range access: {pixbuff[5]}")

    print(f"Before bacon wrap: {pixbuff[0:4]}")
    pixbuff[3]='bacon'
    print(f"After bacon wrap: {pixbuff[0:4]}")

    pixbuff[7] = "tomato"


