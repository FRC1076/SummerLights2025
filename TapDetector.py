"""
   Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
   https://github.com/FRC1076 

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
"""
   Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
   https://github.com/FRC1076 

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import time
import board
from adafruit_circuitplayground import cp

class TapDetector:
    """
    Drop this into code.py and run it standalone.
    It runs for about 10 seconds.   If you tap the top of the CPB, it
    should report the taps with a print statement.

    Like this:
        Time:  111 Detected:  acceleration(x=2.56641, y=-21.9486, z=2.64302)
        Time:  157 Detected:  acceleration(x=-5.97553, y=38.8793, z=-39.6837)
        Time:  184 Detected:  acceleration(x=0.229828, y=-17.2371, z=1.07253)
        ...
        Time:  451 Detected:  acceleration(x=0.804398, y=-15.3219, z=5.36266)

    """
    def __init__(self, max_mute_lifetime=10, tap_threshold=12):
        """
        Vertical orientation is assumed to be writing on the back upright or else
        upside down.  Use abs() to cover both orientations, checking the value of y acceleration
        """
        self._max_mute_lifetime = max_mute_lifetime
        self._mute_lifetime = 0
        self._tap_threshold = tap_threshold
        self._tap_detected = None
        self._last_reading = None
        # Initialize the I2C bus. The Circuit Playground Bluefruit uses the default I2C pins.
        #i2c = board.I2C()

        # Initialize the LIS3DH accelerometer (limit to 2G)
        #self._accel = adafruit_lis3dh.LIS3DH(i2c)
        #self._accel.range = adafruit_lis3dh.RANGE_2_G

    def sense(self):
            """
            Extract acceleration, respect mute, determine if threshold exceeded
            """
            self._tap_detected = False
            self._last_reading = (x, y, z) = cp.acceleration

            """
            After a tap, mute in order to debounce a little bit
            """
            if self._mute_lifetime > 0:
                self._mute_lifetime -= 1
                return

            """
            On tap, record detection, start mute
            Detection only ever lives for a single cycle
            """
            if abs(y) > self._tap_threshold:
                self._tap_detected = True
                self._mute_lifetime = self._max_mute_lifetime


    def gotTapped(self):
        return self._tap_detected

    def lastReading(self):
        return self._last_reading


if __name__ == "__main__":

    det = TapDetector()

    for t in range(500):

        det.sense()
        if det.gotTapped():
            print("Time: ", t, "Detected: ", det.lastReading())
        time.sleep(0.02)
