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

    def Nple_pixels(self, pixel_size):
        """
        Double up or triple up pixels of a topological grouping composition
        """
        c = self._composition

        if pixel_size == 2:
            return [ c[i*2]+c[i*2+1] for i in range(len(c)//2) ]
        elif pixel_size == 3:
            return [ c[i*3]+c[i*3+1]+c[i*3+2] for i in range(len(c)//3) ]
        else:
            return c

    def digit7HSlices(self):
        """
        Horizontal slices to make grouped pixels for vertical effects
        Works only for the x pixel Seven Digit
        """
        top = [ (77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93), (76, 94), (0, 75), (1, 74), (59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73), (58, 2, 3) ]
        tail = [ (4+i, 57-i) for i in range(27) ]

        self._composition = top + tail
        rows = len(self._composition)
        return rows

    def digit7VSlices(self):
        """
        Vertical slices to make grouped pixels for vertical effects
        Works only for the x pixel Seven Digit
        """
        left = [ (73, 74, 75, 76) ]
        layer1 = [ (72-i, 77+i) for i in range(3) ]
        layer2 = [ (32, 69, 80), (31, 33, 34, 35, 68, 81), (36, 67, 82), (30, 37, 38, 39, 66, 83), (29, 40, 41, 65, 84), (28, 27, 26, 42, 43, 44, 64, 85) ]
        layer3 = [ (24, 25, 45, 46, 63, 86), (23, 22, 21, 20, 47, 48, 49, 50, 51, 62, 87, 88), (19, 18, 17, 52, 53, 54, 55, 60, 89), (13, 14, 15, 16, 56, 57, 58, 59, 90) ]
        right = [ (10, 11, 12, 91), (8, 9, 92), (7, 5, 6, 93), (3, 4, 94), (0, 1, 2) ]

        self._composition = left + layer1 + layer2 + layer3 + right
        columns = len (self._composition)
        return columns

    def digit7Strokes(self):
        """
        Slices to simulate a writing stroke
        """
        start = [ (73, 74, 75, 76) ]
        layer1 = [ (72-i, 77+i) for i in range(13) ]
        layer2 = [ (59, 90, 91, 92, 93, 94), (58, 0, 1, 2, 3) ]
        end = [ (4+i, 57-i) for i in range(27) ]

        self._composition = start + layer1 + layer2 + end
        strokes = len(self._composition)
        return strokes

    def digit0HSlices(self):
        """
        Horizontal slices to make grouped pixels for vertical effects
        Works only for the x pixel Zero Digit
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

    def digit0VSlices(self):
        """
        Vertical slices to make grouped pixels for vertical effects
        Works only for the x pixel Zero Digit
        """
        left = [ (72, 73, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9), (70, 71, 10, 11), (68, 69, 12, 13), (66, 67, 14, 15), (65, 127, 128, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 16) ]
        layer1 = [ (64, 124, 125, 126, 84, 85, 86, 17, 18), (63, 123, 87, 88, 19) ]
        layer2 = [ (62-i, 122-i, 89+i, 20+i) for i in range (7) ]
        layer3 = [ (55, 114, 115, 97, 98, 27), (54, 113, 112, 99, 98, 28), (53, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 29)]
        layer4 = [ (52-i, 30+i) for i in range (4) ]
        right = [ (34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48) ]

        self._composition = left + layer1 + layer2 + layer3 + layer4 + right
        columns = len(self._composition)
        return columns

    def digit0Strokes(self):
        """
        Slices to simulate a writing stroke
        """
        start = [ (0+i, 74+i) for i in range(9) ]
        layer1 = [ (9, 10, 83), (11, 84), (12, 13, 85), (14, 86), (15, 16, 87), (17, 18, 19, 88)]
        layer2 = [ (20+i, 89+i) for i in range(4) ]
        layer3 = [ (24, 25, 93), (26, 27, 94), (28, 29, 95), (30, 31, 96) ]
        layer4 = [ (97+i, 32+i) for i in range(14) ]
        layer5 = [ (111, 46, 47), (112, 48, 49), (113, 50), (114, 51), (115, 52, 53), (116, 54, 55), (117, 56), (118, 57, 58) ]
        layer6 = [ (119+i, 59+i) for i in range(5) ]
        end = [ (124, 64, 65), (125, 66, 67), (126, 68, 69), (127, 70, 71), (128, 72, 73) ]

        self._composition = start + layer1 + layer2 + layer3 + layer4 + layer5 + layer6 + end
        strokes = len(self._composition)
        return strokes

    def digit1HSlices(self, pixel_size=2):
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
        self._composition = self.Nple_pixels(pixel_size)
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

    def digit1Strokes(self,pixel_size=3):
        """
        Slices to simulate a writing stroke (18)
        """
        nose = [ (44-i, 45+i) for i in range(11) ]
        transition = [ tuple(33-i for i in range(9)) ]
        stem = [ (26-i, 54+i) for i in range(23) ]
        bottom = [ (77, 0, 1, 2, 3) ]
        self._composition = nose + transition + stem + bottom
        self._composition = self.Nple_pixels(pixel_size)
        strokes = len(self._composition)
        return strokes

    def digit6HSlices(self):
        pass
    def digit6VSlices(self):
        pass
    def digit6Strokes(self):
        pass
        
    def digit7HSlices(self):
        pass
    def digit7VSlices(self):
        pass
    def digit7Strokes(self):
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


