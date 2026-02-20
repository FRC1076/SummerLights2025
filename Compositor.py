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

from PixelBuffer import PixelBuffer

class Compositor:

    def __init__(self):
        self._composition = None
        self._buffer_list = None

    def setBufferList(self, list_of_buffers):
        self._composition = list_of_buffers

    def buffer_list(self):
        return self._composition

    def passThru(self, num_pixels):
        self._composition = [ i for i in range(num_pixels) ]

    def groupsOfN(self, num_pixels, num_groups=2):
        """
        Group NUM_PIXELS pixels into NUM_GROUPS, producing NUM_PIXELS//NUM_GROUPS groups of pixels
        each pixel in the group of pixels takes on the same value set on the group.

        For example:
            Compositor.GroupsOFN(120, 12)

            Produces a Compositor that presents a 12 value pixel buffer, with each value controlling 10
            successive neo_pixels.
        """
        assert (num_pixels % num_groups) == 0,  "Groups must evenly divide pixels, try 2, 3, 4, 5, 6 and multiples"
        group_size = num_pixels // num_groups
        start_index = 0
        group_list = [ ]
        for i in range(num_groups):
            group_list.append([ j for j in range(start_index, (i+1)*group_size) ])
            start_index += group_size

        self._composition = group_list


    def divisionsOfN(self, num_pixels, num_divisions=2):
        """
        """
        assert (num_pixels % num_divisions) == 0,  "Divisions must evenly divide pixels, try 2, 3, 4, 5, 6 and multiples"
        division_size = num_pixels // num_divisions
        buffer_list = [ PixelBuffer(division_size) for i in range(num_divisions) ]

        self._composition = buffer_list

    def frameNcorners(self):
        #  [ [15*i+j+4] for i in range(4) for j in range(10) ]
        top = [ [4], [5], [6], [7], [8], [9], [10], [11], [12], [13] ]
        right = [ [19], [20], [21], [22], [23], [24], [25], [26], [27], [28] ]
        btm = [ [34], [35], [36], [37], [38], [39], [40], [41], [42], [43] ]
        left = [ [49], [50], [51], [52], [53], [54], [55], [56], [57], [58] ]
        topleft = [ [58], [59], [0], [1], [2] ]
        topright = [ [14], [15], [16], [17], [18] ]
        btmright = [ [29], [30], [31], [32], [33] ]
        btmleft = [ [44], [45], [46], [47], [48] ]
        self._composition = top + right + btm + left + topleft + topright + btmright + btmleft

    def featherRows(self):
        self._composition = [ [i for i in range(8*j-8,8*j)] for j in range(1,5) ]

    def featherCols(self, cols):
        self._composition = [ [ i, i+8, i+16, i+24 ] for i in range(cols) ]

    def eightHorizontal(self, rows):
        lc = 66
        rc = lc + 2
        first_part = [ [ lc-2*i, lc-2*i+1, rc+2*i, rc+2*i+1 ] for i in range(14) ]
        second_part = [ [ lc-2*i, lc-2*i+1, 119-4*(i-14), 118-4*(i-14), 117-4*(i-14), 116-4*(i-14), 99+4*(i-14), 98+4*(i-14), 97+4*(i-14), 96+4*(i-14), 2*(i-14), 2*(i-14)+1 ] for i in range(14, 17) ]
        third_part = [ [ 33-2*(i-17), 33-2*(i-17)-1, 6+2*(i-17), 6+2*(i-17)+1 ] for i in range(17, 24) ]

        self._composition = first_part + second_part + third_part

    def oval(self, num_pixels, rows):
        self._composition = [ [ i, num_pixels-i-1 ] for i in range(rows) ]

    def __len__(self):
        return len(self._composition)

    def compose(self, pixel_buffer, neo_pixels):
        """
        Compose all of the pixel_buffer elements into the neo_pixels data model.
        The value at pixel_buffer[i] will get copied to neo_pixels[composition[i]] if composition[i] is a number.
        If the composition[i] is a list, then the value at pixel_buffer[i] will be copied to all neo_pixels[j] for j in composition[i]
        """
        global_index=0

        #if isinstance(self._composition[0], int):
        #    for i in range(len(self._composition)):
        #        neo_pixels[i] = pixel_buffer[i]
        #return
        for i,c in enumerate(self._composition):
            if isinstance(c, int):
                neo_pixels[i] = pixel_buffer[i]
            elif isinstance(c, PixelBuffer):
                """
                Concatenate each PixelBuffer into the neo_pixels, one after another
                """
                for j in range(len(c)):
                    #print(f"neopixels[{(j+global_index):d}]=c[{i}][{j:d}]={c[j]}")
                    neo_pixels[j+global_index] = c[j]
                global_index += len(c)
            elif isinstance(c, list):
                """
                Copy the same buffer value to all of the member pixels of the group
                """
                for j in c:
                    neo_pixels[j] = pixel_buffer[i]


