from PixelBuffer import PixelBuffer

class Compositor:

    def __init__(self):
        self._composition = None

    def bufferList(self, list_of_buffers):
        self._composition = list_of_buffers

    def passThru(self, num_pixels):
        self._composition = [ i for i in range(num_pixels) ]

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
        print(self._composition)

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


