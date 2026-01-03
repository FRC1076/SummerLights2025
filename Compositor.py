class Compositor:

    def __init__(self):
        self._composition = None

    def passThru(self, num_pixels):
        self._composition = [i for i in range(num_pixels)]

    def featherColumns(self):
        self._composition = [ [i for i in range(4*j-4,4*j)] for j in range(1,9) ]

    def compose(pixel_buffer, neo_pixels):
        """
        Compose all of the pixel_buffer elements into the neo_pixels data model.
        The value at pixel_buffer[i] will get copied to neo_pixels[composition[i]] if composition[i] is a number.
        If the composition[i] is a list, then the value at pixel_buffer[i] will be copied to all neo_pixels[j] for j in composition[i]
        """
        for i,c in enumerate(self._composition):
            if isinstance(c, int):
                neo_pixels[i] = pixel_buffer[i]
            elif isinstance(c, list):
                for j in c:
                    neo_pixels[j] = pixel_buffer[i]
                
