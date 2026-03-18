import board
import microcontroller
import binascii

# model of the board
boardID = board.board_id
# model 
boardName = binascii.hexlify(microcontroller.cpu.uid).decode()
# what number is the board in (defulted to 300 as it's not a acceptable number )
boardNumber = "defualt"

# defualts NEO_PIN to GP15
NEO_PIN = board.GP15

# changes the value of NEO_PIN based off the model of the board 
if boardID == "adafruit_kb2040":
    NEO_PIN = board.D2
elif boardID == "circuitplayground_bluefruit":
    NEO_PIN = board.D10
elif boardID == "raspberry_pi_pico2":
    NEO_PIN = board.GP15
elif boardID == "adafruit_feather_rp2040":
    NEO_PIN = board.D6

boardNumDictionary = {
     "0000000000000000" : "1",
     "pass" : "0",
     "pass" : "7",
     "pass" : "6"
     }

boardNumber = boardNumDictionary[boardName]

class HardwareAwareness:

    def __init__(self):
        pass
    