import board
import neopixel
import digitalio
import time

FEATHER_WING_ROWS = 4
FEATHER_WING_COLUMNS = 8

# Two choices for strings
FEATHER_WING_PIXELS = FEATHER_WING_ROWS * FEATHER_WING_COLUMNS
NEON_PIXELS = 64

# Choose which we are using
NUM_PIXELS = FEATHER_WING_PIXELS

# Useful global constants
COLOR_INC = 255 / NUM_PIXELS                  # color increment to cycle through color range across all pixels
BRIGHTNESS = 0.1

OFF = (0, 0, 0)
PURPLE = (92, 50, 168)
ORANGE = (235, 122, 52)
BLUE = (24, 30, 214)


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

 
class MatrixDisplayMapper:
    """
    (0,0)              (0,1)             ...                   (0, num_cols-1)
    ...
    (num_rows-2, 0)
    (num_rows-1, 0)    (num_rows-1, 1)   ...          (num_rows-1, num_cols-1)
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
        
        return r*self._num_cols+c
    
    def would_leave_screen(self, coords, vector):
        """
        Return None if the point at coords would leave the screen.
        Otherwise return the new vector resulting from a bounce at the edge
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
   
    def __init__(self, pixels, displaymap, color=BLUE, clear_on_init=False):
        """
        This bouncing ball effect works on a neopixel string or matrix that has a map
        The zero indexed pixel represents the origin at 0,0 (upper right)
        """
        self._pixels = pixels
        self._color = color
        self._vect = (1, 1)
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
    bounce_effect = OnePixelBall(pixels, displaymap=neofeather, color=ORANGE, clear_on_init=False)
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

