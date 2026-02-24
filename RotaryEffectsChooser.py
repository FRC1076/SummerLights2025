import board
import neopixel
import rotaryio
import digitalio

encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1)
pixels = neopixel.NeoPixel(board.GP6, 32, brightness=0.05, auto_write=False)

class SevenSegment:    
    # Bit pattern covers a thru h values with a being the LSB
    ERROR = 0x36
    #                  0     1     2     3     4     5     6     7     8     9     A     b     c     d     E     F
    DisplayData = [ 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7C, 0x07, 0x7F, 0x6F, 0x77, 0x7C, 0x58, 0x5E, 0x79, 0x71 ]
    
    def __init__(self, pins):
        """
        The array of pins covers the a,b,c,d,e,f,g,dp pins for the 7 segment
        plus the decimal point.
        """
        self._pins = pins
        self._segments = [ digitalio.DigitalInOut(p) for p in pins ]
        
        for s in self._segments:
            s.direction = digitalio.Direction.OUTPUT
        
    def display(self, value):        
        try:
            bits = SevenSegment.DisplayData[value]
        except IndexError:
            bits = DisplayData.ERROR
        
        print(hex(bits))
        for p in range(len(self._segments)):
            if (bits & 0x1) == 1:
                self._segments[p].value = True
            else:
                self._segments[p].value = False
            bits = bits >> 1
            

def signum(a, b):
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

#                             a            b           c           d           e           f           g
segments = SevenSegment([ board.GP14, board.GP15, board.GP17, board.GP18, board.GP19, board.GP13, board.GP12 ])
last_position = None
while True:
    position = encoder.position
    if last_position is None or position != last_position:
        if last_position is None:
            setting = 0
        else:
            setting = ((setting + signum(last_position,position)) % 16)         
        print(setting)
        
        pixels.fill((0,0,0))
        for i in range(setting+1):
            pixels[i]=(200, 0, 200)
        pixels.show()
        segments.display(setting)
        
    last_position = position
    
