class LightingEffect_Base:
    """
    To run a lighting effect, you need to (1) create the effect (associating it with all or
    part of the light string), (2) call the make_generator method to create the generator object
    (3) call next on the generator until it terminates.

    import time
    import board
    import neopixel
    
    pixels = neopixel.NeoPixel(board.GP6, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    pixels.fill((0,0,0))
    blinky_effect = LightingEffect_Base(pixels, 0, NUM_PIXELS)   # specify more to override default values
    blinky_gen = blinky_effect.make_generator()

    finished = False
    while not finished:
        try:
            next(blinky_gen)
            pixels.show()
            time.sleep(0.20)
        except StopIteration:
            finished = True
            
    """
    def __init__(self, pixels, start_index, num_pixels, color=PURPLE, brightness=BRIGHTNESS, slowness=10, clear_on_init=True):
        """
        Base class for lighting effects
        Could be useful for documentation, or maybe actually used as a base class
        Note, this relies on constants from elsewhere.    Should probably import them instead of assuming
        they have been imported.
        """
        self._pixels = pixels
        self._start_index = start_index
        self._num_pixels = num_pixels
        self._color = color
        self._brightness = brightness
        self._slowness = slowness

        if clear_on_init:
            self.clear_all(OFF)

    def clear_all(pixels, start, length):
        """
        Static function that any class can use.
        """
        for p in range(start, start+length):
            pixels[p] = OFF

    def clear_all_in_my_domain(self):
        """
        Zero out everything in our domain
        """
        clear_all(self._pixels, self._start_index, self._num_pixels)

    def make_generator(self):
        """
        Make blinky the default application
        """
        while True:
            for p in range(self._start_index, self._start_index+self._num_pixels):
                pixels[p] = self._color

            for _ in range(self._slowness):
                yield

            for p in range(self._start_index, self._start_index+self._num_pixels):
                pixels[p] = OFF

            for _ in range(self._slowness):
                yield
        

class WipeFillEffect:
    """
    Fills num_pixels starting at start_index with the specified color.
    *
    **
    ***
    ...
    ***********

    The effect yields after every frame (line in the animation above) so the wipe is animated.
    """
    def __init__(self, pixels, start_index, num_pixels, color=PURPLE, brightness=BRIGHTNESS,  slowness=2, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 50hz using a python generator to break up the updates
        """
        self._pixels = pixels
        self._start_index = start_index
        self._num_pixels = num_pixels
        self._color = color
        self._brightness = brightness
        self._slowness = slowness
        
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
        for _ in range(self._num_pixels):
            self._pixels[p] = self._color
            p += 1
            """
            The yield command here, turns this function into a generator, so it returns after each
            iteration of the loop.   Subsequent calls pick up where they left off.
            """
            for _ in range(self._slowness):
                yield


class SqueezeFillEffect:
    """
    Fills from both directions at the same speed
    *        *
    **      **
    ***    ***
    ****  ****
    **********
    """
    def __init__(self, pixels, start_index, num_pixels, color=PURPLE, brightness=BRIGHTNESS, slowness=2, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done at 20hz using a python generator to break up the updates
        """
        self._pixels = pixels
        self._start_index = start_index
        self._num_pixels = num_pixels
        self._color = color
        self._brightness = brightness
        self._slowness = slowness

        if clear_on_init:
            """
            But, do not display, just zero out everything in our domain
            """
            for p in range(self._start_index, self._start_index+self._num_pixels):
                self._pixels[p] = OFF

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
    
    def __init__(self, pixels, start_index, num_pixels, color=PURPLE, brightness=BRIGHTNESS, slowness=0, clear_on_init=True):
        """
        Create a lighting effect that fills PIXELS in the specified range, with the specified color.
        Defaults are all PURPLE pixels at the global BRIGHTNESS.
        The filling is done all in one shot, suitable for use as a background for some other effect.
        """
        self._pixels = pixels
        self._start_index = start_index
        self._num_pixels = num_pixels
        self._pixel_range = pixel_range
        self._color = color
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
        p = 0
        for p in self._pixel_range:
            self._pixels[p] = self._color
        


class OnePixelCar:
    """
    One pixel car drives from low to high on the string.
    This effect does it's own repair of the background.
    That could be a service provided by the graphics buffer.
    """
    def __init__(self, pixels, pixel_range=range(NUM_PIXELS), color=BLUE, clear_on_init=False):
        self._pixels = pixels
        self._color = color
        self._pixel_range = pixel_range
        self._repair_index = None
        self._repair_value = None
        
    def make_generator(self, slowness=2):
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


class MatrixDisplayMapper:
    """
    Here is the map.   Each element is (row, col)
    --------------------------------------------------------------------------
    (0,0)              (0,1)             ...                   (0, num_cols-1)
    (1,0)              (1,1)             ...                   (1, num_cols-1)
    ...
    (num_rows-2, 0)    (num_rows-2, 1)   ...          (num_rows-2, num_cols-1)
    (num_rows-1, 0)    (num_rows-1, 1)   ...          (num_rows-1, num_cols-1)
    --------------------------------------------------------------------------
    """
    
    def __init__(self, num_rows, num_cols):
        self._num_rows = num_rows
        self._num_cols = num_cols
    
    @staticmethod
    def clamp(value, min_val, max_val):
        """Clamps a value within a specified range."""
        return max(min(value, max_val), min_val)

    
    def rowcol_to_ndx(self, coords):
        # make sure the row and column are in bounds (between 0 and N-1)
        r = MatrixDisplayMapper.clamp(coords[0], 0, self._num_rows-1)
        c = MatrixDisplayMapper.clamp(coords[1], 0, self._num_cols-1)
        
        # snap row to integer grid so the math works
        return int(round(r)*self._num_cols+c)
    
    def would_leave_screen(self, coords, vector):
        """
        Return None if the point at coords would leave the screen.
        Otherwise return the new vector resulting from a bounce at the boundary
        """
        row_vect = None
        col_vect = None
        
        # would leave through the top edge
        if coords[0]+vector[0] < 0:
            row_vect = -vector[0]
        # would leave through the bottom e
        elif coords[0]+vector[0] >= self._num_rows:
            row_vect = -vector[0]
        
        # would leave through the left edge
        if coords[1]+vector[1] < 0:
            col_vect = -vector[1]
        # would leave through the right edge
        elif coords[1]+vector[1] >= self._num_cols:
            col_vect = -vector[1]
    
        # if there is no hitting an edge, the vector does not change
        new_row_vect = vector[0] if row_vect is None else row_vect
        new_col_vect = vector[1] if col_vect is None else col_vect
        
        # if neither hits and edge
        if row_vect is None and col_vect is None:
            return None
        else:
            return (new_row_vect, new_col_vect)
        
 
class OnePixelBall:
   
    def __init__(self, pixels, displaymap, vect=(1, 1), color=BLUE, clear_on_init=False):
        """
        This bouncing ball effect works on a neopixel string or matrix that has a map
        The zero indexed pixel represents the origin at 0,0 (upper right)
        """
        self._pixels = pixels
        self._color = color
        self._vect = vect
        self._rowcol = (0, 0)
        self._displaymap = displaymap
        self._repair_index = None
        self._repair_value = None
        
    def runner(self, slowness=2):
        #
        #  Ball bounces around forever.
        #
        while True:
            
            # repair the damage from the previous frame
            if self._repair_index != None:
                self._pixels[self._repair_index] = self._repair_value
                
            # before we draw the ball at rowcol, save the repair info
            ndx = self._displaymap.rowcol_to_ndx(self._rowcol)
            self._repair_index = ndx
            self._repair_value = self._pixels[ndx]
            
            # draw the ball at the computed index
            self._pixels[ndx] = self._color
            
            # see if the ball can move to the next location, or if it bounces at the boundary
            next_vect = self._displaymap.would_leave_screen(self._rowcol, self._vect)
            
            # if there is a collision, update the new vector
            if not next_vect is None:
                self._vect = next_vect
            
            # compute the next position for the ball
            next_row = self._rowcol[0] + self._vect[0]
            next_col = self._rowcol[1] + self._vect[1]
            self._rowcol = (next_row, next_col)
            
            # run at designated speed
            for _ in range(slowness):
                yield
        

if __name__ == "__main__":
    
    
    # Initialize the neopixel model and clear it
    pixels = neopixel.NeoPixel(board.GP6, NUM_PIXELS, brightness = BRIGHTNESS, auto_write = False)
    pixels.fill((0,0,0))

    """
    One time setup with solid PURPLE
    """
    print("Display background once")
    purple_background_effect = InstantFillBackground(pixels, color=OFF)
    
    """
    Bouncing ball effect works in 2D space, so use a display mapper to manage the 2D space
    """
    neofeather = MatrixDisplayMapper(4, 8)
    bounce_effect = OnePixelBall(pixels, displaymap=neofeather, vect=(0.2, 0.3), color=ORANGE, clear_on_init=False)
    do_bouncing_ball = bounce_effect.runner()
    
    # Draw the background, then wait for a bit to create suspense
    purple_background_effect.run()
    pixels.show()
    time.sleep(3)
    
    while True:
        # bouncing ball effect runs forever
        next(do_bouncing_ball)
        pixels.show()
        time.sleep(0.02)
    
