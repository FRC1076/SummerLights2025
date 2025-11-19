class SqueezeFillEffect:

    def __init__(self, pixels, start_index, num_pixels, color=PURPLE, slowness=2, brightness=BRIGHTNESS, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 20hz using a python generator to break up the updates
        """
        self._pixels = pixels
        self._start_index = start_index
        self._num_pixels = num_pixels
        self._color = color
        self._slowness = slowness
        self._brightness = brightness

        if clear_on_init:
            """
            But, do not display, just zero out everything
            """
            pixels.fill(OFF)

    def make_generator(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        p = self._start_index
        for _ in range(self._num_pixels/2):
            self._pixels[p] = self._color
            self._pixels[self._num_pixels - 1 - p] = self._color
            p += 1
            """
            The yield command here, turns this function into a generator, so it returns after each
            iteration of the loop.   Subsequent calls pick up where they left off.
            """
            for _ in range(self._slowness):
                yield


class InstantFillBackground:
    
    def __init__(self, pixels, pixel_range=range(NUM_PIXELS), color=PURPLE, brightness=BRIGHTNESS, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done all in one shot, suitable for use as a background for some other effect.
        """
        self._pixels = pixels
        self._pixel_range = pixel_range
        self._color = color
        self._brightness = brightness
        
        if clear_on_init:
            """
            But, do not display, just zero out everything
            """
            pixels.fill(OFF)
            
    def run(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        for p in self._pixel_range:
            self._pixels[p] = self._color
        


class WipeFillBackground:
    
    def __init__(self, pixels, pixel_range=range(NUM_PIXELS), color=PURPLE, brightness=BRIGHTNESS, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 50hz using a python generator to break up the updates
        """
        self._pixels = pixels
        self._pixel_range = pixel_range
        self._color = color
        self._brightness = brightness
        
        if clear_on_init:
            """
            But, do not display, just zero out everything
            """
            pixels.fill(OFF)
            
    def runner(self):
        """
        Need to decide how to set the brightness separately
        maybe just scale the self._color on __init__?
        or just agree to use the color passed in
        """
        for p in self._pixel_range:
            self._pixels[p] = self._color
            """
            The yield command here, turns this function into a generator, so it returns after each
            iteration of the loop.   Subsequent calls pick up where they left off.
            """
            yield p


class OnePixelCar:
   
    def __init__(self, pixels, pixel_range=range(NUM_PIXELS), color=BLUE, clear_on_init=False):
        self._pixels = pixels
        self._color = color
        self._pixel_range = pixel_range
        self._repair_index = None
        self._repair_value = None
        
    def runner(self, slowness=2):
        """
        Car can run slower, e.g. slowness = 50 to run 1 pixel per second
        Slowess=1 is a bit too hard to see
        """
        for carpos in self._pixel_range:
            
            # repair the damage from the previous frame
            if self._repair_index != None:
                self._pixels[self._repair_index] = self._repair_value
            
            # before we draw the car at carpos, save the repair info
            self._repair_index = carpos
            self._repair_value = self._pixels[carpos]
            
            # draw the car
            self._pixels[carpos] = self._color
            
            # run at designated speed
            for _ in range(slowness):
                yield

