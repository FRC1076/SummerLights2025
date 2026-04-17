import microcontroller
import binascii
import board

#  Example only.   Data may not be correct.   Serial numbers are, and I WILL USE the first one for the "1" digit
digit_dict = {  '9c269e8c931ea92c' : { "index": 0, "name": "1", "neo_pin": board.D10, "num_pixels": 78 },
                '7e75345dc17e7eac' : { "index": 1, "name": "0", "neo_pin": board.D10, "num_pixels": 128 } }

#
# Other serial numbers: (marked on the devices)
# Put the extras in the table and mark them as spares
#
# e5e0340e79345125
# 28d7e12692c1b153
# dfa90633b8e2ed5a
# 030f3ec3f2755aaf

# Get the unique CPU ID
serial_number = microcontroller.cpu.uid

# Convert it to a readable hexadecimal string
formatted_serial = binascii.hexlify(serial_number).decode()

serial = str(formatted_serial)

print("Serial Number:", serial)

try:
    print(digit_dict[serial])
except KeyError as ke:
    print("Key not found:", str(ke))
    serial = '9c269e8c931ea92c'
    print(f"Setting to a good key: {serial} to support this example.")


print(digit_dict[serial])


digit_config = digit_dict[serial]

print("Name:", digit_config["name"])
print("Neo_pin:", digit_config["neo_pin"])
