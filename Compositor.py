"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076
https://github.com/FRC1076
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

    def digit0HSlices(self)
        """
        Horizontal slices to make grouped pixels for vertical effects
        Works only for the 78 pixel Zero Digit
        """
        top = [ (20, 21, 22, 23, 24) ]
        layer1 = [ (19-i, 25+i) for i in range(4) ]
        layer2 = [ (15, 29, 90, 91, 92), (14, 30, 88, 89, 93, 94) ]
        layer3 = [ (13-i, 31+i, 87-i, 95+i) for i in range(14) ]
        layer4 = [ (109, 45), (110, 73) ]
        layer5 = [ (72-i, 128-i, 111+i, 46+i) for i in range(6) ]
        layer6 = [ (66, 121, 122, 117, 118, 52), (53, 65, 119, 120) ]
        layer7 = [ (54+i, 64-i) for i in range (4) ]
        bottom = [ (58, 59, 60) ]

        self._composition = top + layer1 + layer2 + layer3 + layer4 + layer5 + layer6 + layer7 + bottom
        rows = len(self._composition)
        # print("digit0H", self._composition)
        # assert(len(self.composition) == rows)
        return rows

    def digit1HSlices(self):
        """
        Horizontal slices to make grouped pixels for vertical effects
        Works only for the 78 pixel One Digit
        """
        top = [ (31, 32, 33), (30, 34), (35,), (29, 36), (28,37), (27,38),
                (39,), (26, 40, 53), (41, 52, 54), (25, 42, 51, 55 ), (24, 43, 50),
                (23, 49, 56), (44, 48, 57), (22, 47), (45, 46, 58) ]
        middle = [ (21-i, 59+i) for i in range(18) ]
        bottom = [ (77,), (3,), (0, 1, 2) ]

        self._composition = top + middle + bottom
        rows = len(self._composition)
        return rows

    def digit1VSlices(self):
        """
        Vertical slices to support wipe from side to side. (36)
        """
        nose = [ (44,), (45,), (43,), (42,) ]
        transition = [ (41-i, 46+i) for i in range(8) ]
        left_edge = [ tuple(53+i for i in range(25)) ]
        top_and_bottom = [ (33-i, i) for i in range(4) ]
        right_edge = [ tuple(i+4 for i in range(26)) ]
        self._composition = nose + transition + left_edge + top_and_bottom + right_edge

        columns = len(self._composition)
        return columns

    def digit1Strokes(self):
        """
        Slices to simulate a writing stroke (18)
        """
        nose = [ (44-i, 45+i) for i in range(11) ]
        transition = [ tuple(33-i for i in range(9)) ]
        stem = [ (26-i, 54+i) for i in range(23) ]
        bottom = [ (77, 0, 1, 2, 3) ]
        self._composition = nose + transition + stem + bottom

        strokes = len(self._composition)
        return strokes

    def digit0HSlices(self):
        pass
    def digit0VSlices(self):
        pass
    def digit0Strokes(self):
        pass

    def digit7HSlices(self):
        pass
    def digit7VSlices(self):
        pass
    def digit7Strokes(self):
        pass

    def digit6HSlices(self):
        pass
    def digit6VSlices(self):
        pass
    def digit6Strokes(self):
        pass

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
                try:
                    neo_pixels[i] = pixel_buffer[i]
                except IndexError:
                    pass
            elif isinstance(c, PixelBuffer):
                """
                Concatenate each PixelBuffer into the neo_pixels, one after another
                """
                for j in range(len(c)):
                    #print(f"neopixels[{(j+global_index):d}]=c[{i}][{j:d}]={c[j]}")
                    try:
                        neo_pixels[j+global_index] = c[j]
                    except IndexError:
                        pass
                global_index += len(c)
            elif isinstance(c, list) or isinstance(c, tuple):
                """
                Copy the same buffer value to all of the member pixels of the group
                """
                for j in c:
                    try:
                        neo_pixels[j] = pixel_buffer[i]
                    except IndexError:
                        pass


