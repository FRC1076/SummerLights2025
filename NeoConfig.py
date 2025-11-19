FEATHER_WING_ROWS = 4
FEATHER_WING_COLUMNS = 8

# Two choices for strings
FEATHER_WING_PIXELS = FEATHER_WING_ROWS * FEATHER_WING_COLUMNS
NEON_PIXELS = 64

# Choose which we are using
NUM_PIXELS = FEATHER_WING_PIXELS

# Useful global constants

# color increment ensures that we can cycle through a full
# range of color intensities from the first to last pixels
COLOR_INC = 255 / NUM_PIXELS

# keep things dim to save power
BRIGHTNESS = 0.1

# some ready made colors (feel free to add more)
OFF = (0, 0, 0)
PURPLE = (92, 50, 168)
ORANGE = (235, 122, 52)
BLUE = (24, 30, 214)
BUTTERSCOTCH = (252, 186, 3)
GREEN = (3, 252, 92)
PINK = (248, 3, 252)
