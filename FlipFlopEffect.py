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

