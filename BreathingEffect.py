import math
from NeoConfig import FPS

class BreathingEffect:

    BREATH_SECS = 6
    MIN_BRIGHTNESS = 0.05
    MAX_BRIGHTNESS = 1.0

    def __init__(self, pixel_buffer, color=(255, 0, 255),brightness=MAX_BRIGHTNESS, slowness=1):
        self._pixel_buffer = pixel_buffer
        self._color = color
        self._brightness = brightness
        self._slowness = slowness

        self._steps = int(FPS * BreathingEffect.BREATH_SECS)

        self._brightness_values = []
        for step in range(self._steps):
            radians = (2 * math.pi * step) / self._steps
            normalized = (math.sin(radians) + 1) / 2

            breath_brightness = (
                BreathingEffect.MIN_BRIGHTNESS +
                normalized * (BreathingEffect.MAX_BRIGHTNESS - BreathingEffect.MIN_BRIGHTNESS)
            )

            final_brightness = breath_brightness * self._brightness
            self._brightness_values.append(final_brightness)

    def _scale_color(self, color, brightness):
        r, g, b = color
        return (
            int(r * brightness),
            int(g * brightness),
            int(b * brightness)
        )

    def make_generator(self):
        while True:
            for brightness in self._brightness_values:
                scaled = self._scale_color(self._color, brightness)

                self._pixel_buffer.fill(scaled)
                self._pixel_buffer.show()

                # run at the requested speed
                for _ in range(self._slowness):
                    yield