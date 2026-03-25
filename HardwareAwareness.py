import board
import microcontroller
import binascii
import neopixel
from NeoConfig import BRIGHTNESS, WOKWI_BRIGHTNESS


class HardwareAwareness:

    # model
    boardName = binascii.hexlify(microcontroller.cpu.uid).decode()
    # what number is the board in (defulted to 300 as it's not a acceptable number )

    boardNumDictionary = {
        "dfa90633b8e2ed5a" : {"index": 0, "name": "1", "brightness": BRIGHTNESS},
        "9c269e8c931ea92c" : {"index": 1, "name": "0", "brightness": BRIGHTNESS},
        "e5e0340e79345125" : {"index": 2, "name": "7", "brightness": BRIGHTNESS},
        "030f3ec3f2755aaf" : {"index": 3, "name": "6", "brightness": BRIGHTNESS},
        "7e75345dc17e7eac" : {"index": 4, "name": "Reserved", "brightness": None},
        "0000000000000000" : {"index": 0, "name": "wokwi", "brightness": WOKWI_BRIGHTNESS},
        # 28d7e12692c1b153
    }

    numPixelsList = [ 78, 128, 96, 112 ]

    def __init__(self, forceNumPixels=None, forceNeoPin=None):

        self.boardID = board.board_id
        print("BoardID:", self.boardID)
        self._boardName = binascii.hexlify(microcontroller.cpu.uid).decode()
        self._info = HardwareAwareness.boardNumDictionary[self._boardName]
        self._index = self._info["index"]
        self._environment = self._info["name"]
        self._brightness = self._info["brightness"]
        if forceNumPixels is None:
            self.num_pixels = HardwareAwareness.numPixelsList[self._index]
        else:
            self.num_pixels=forceNumPixels
        if forceNeoPin is None:
            self.NEO_PIN=self.getNeoPinOrigin()
        else:
            self.NEO_PIN=forceNeoPin
        self.pixels = neopixel.NeoPixel(self.NEO_PIN, self.num_pixels, brightness = self._brightness, auto_write = False)

        print("CPU.uid:", self._boardName)
        print("Index:", self._index)
        print("I am:", self._info["name"])

    # changes the value of NEO_PIN based off the model of the board
    def getNeoPinOrigin(self):

        # There is no safe default
        NEO_PIN = None

        if self.boardID == "adafruit_kb2040":
            NEO_PIN = board.D2
        elif self.boardID == "circuitplayground_bluefruit":
            NEO_PIN = board.D10
        elif self.boardID == "raspberry_pi_pico2":
            NEO_PIN = board.GP15
        elif self.boardID == "raspberry_pi_pico":
            NEO_PIN = board.GP15
        elif self.boardID == "adafruit_feather_rp2040":
            NEO_PIN = board.D6
        return NEO_PIN

    def getPixels(self):
        return self.pixels

    def getNumPixels(self):
        return len(self.pixels)

    def getIndex(self):
        return self._index

    def getEnvironment(self):
        return self._environment

if __name__ == "__main__":

    index = 1
    HardwareAwareness.boardNumDictionary["0000000000000000"] = {"index": index, "name": "wokwi",}

    hwd = HardwareAwareness()
    print(hwd.getNeoPinOrigin())
    print(HardwareAwareness.boardNumDictionary["0000000000000000"])
    print("len of pixels:", len(hwd.getPixels()))
    try:
        assert(len(hwd.getPixels()) == HardwareAwareness.numPixelsList[index])
    except AssertionError as ea:
        print("Problem:", str(ea))
