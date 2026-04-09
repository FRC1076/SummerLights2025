import time
import math
import board
import neopixel

class BreathingEffect:

    """
    """
    def __init__(self, pixels, color=(255, 0, 255), fps=50, breath_seconds=6,
                 min_brightness=0.05, max_brightness=1.0):
        
        self.pixels = pixels
        self.base_color = color
        self.fps = fps
        self.steps = int(fps * breath_seconds)

        self.brightness_values = []
        for step in range(self.steps):
            radians = (2 * math.pi * step) / self.steps
            normalized = (math.sin(radians) + 1) / 2
            
            brightness = min_brightness + normalized * (max_brightness - min_brightness)
            self.brightness_values.append(brightness)

    def scale_color(self, color, brightness):
        r, g, b = color
        return (
            int(r * brightness),
            int(g * brightness),
            int(b * brightness)
        )

    def make_generator(self):
        """
        Change this to make_generator instead.
        Use yield to return the 
        """
        while True:
            for brightness in self.brightness_values:
                scaled = self.scale_color(self.base_color, brightness)

                self.pixels.fill(scaled)
                self.pixels.show()

                yield



if __name__ == "__main__":

    PIXEL_PIN = board.GP15
    NUM_PIXELS = 64

    pixels = neopixel.NeoPixel(
        PIXEL_PIN,
        NUM_PIXELS,
        auto_write=False
    )

    effect = BreathingEffect(pixels)
    effect_gen = effect.make_generator()

    while True:
        next(effect_gen)
        time.sleep(0.020)
