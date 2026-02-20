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


