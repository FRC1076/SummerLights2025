"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076
https://github.com/FRC1076
"""
from NeoConfig import OFF,PURPLE,ORANGE,BUTTERSCOTCH,BLUE,RED,FULL_RED,GREEN
TAP = 3
NO_TAP = 2

ValidSpeeds =   {"slow" :   20,
                 "medium" :  5,
                 "fast" :    1,
                 "tap" :     TAP,
                 "no-tap" :  NO_TAP}

ValidColors =   {"off": OFF,
                 "purple" : PURPLE,
                 "orange" : ORANGE,
                 "butterscotch" : BUTTERSCOTCH,
                 "blue" : BLUE,
                 "red"  : RED,
                 "full-red" : FULL_RED,
                 "green" :  GREEN
                }

ValidEffects = [ "clear",                 #  clear the display (shortcut with simple reset)
                 "flipflop",              #  switch between two adjacent lights
                 "wipe",                  #  display purple on the whole string
                 "rainbow",               #  rainbow effect on full string
                 "runner",                #  zip back and forth
                 "fliprunner",            #  DOES NOT WORK (Needs richer compositor)
                 "squeeze",               #  close the curtain
                 "gradient",              #  Evan Besirli effect
                 "multi",                 #  several effects on substrings
                 "clap",                  #  still experimental
                 "drip",                  #  physics based particle animation
                 "sound",                 #  sound response demo
                 "flashing",              #  flashing lights (Amber)
                 "multicolor",            #  rainbow color (Amber)
                 "Repeat",                #  repeat the previous sequence of effects
                 "Wait",                  #  wait for a number of seconds  (fast=5, medium=25, slow=100)
                 "Quit",                  #  end the sequence of effects
                 "help" ]

ValidDivisions = [   "2",                  #  2 divisions
                     "3",                  #  3 divisions of equal size
                     "4",                  #
                     "5",                  #
                     "6",                  #  6 sections of equal size
                     "12",                 #  12 divisions of equal size
                     "30",                 #  30 divisions of 4
                     "60"  ]               #  60 divisions of equal size

ValidCompositors = [ "full",               #  pass-thru, single buffer, simplest layout
                     "oval",               #  sliced topology for oval with start/end at top
                     "7segment",           #  sliced 7segment display (figure eight)
                     "frameNcorners",      #  5-buffer layout with sides contiguous
                     "digitH",             #  { 1: 78 pixel, 36 row groupings 0: something else  7: something else, 6: something... }
                     "digitV",             #  { 1: 18 column groupings }
                     "digitS",             #  { 1: 36 stroke groupings }
                     "1/2",                #  split into two pixels
                     "1/4",                #  split into four pixels
                     "1/10" ] + ValidDivisions

def show_help():
    print("effect compositor color [speed | other options]")
    print("Example: flipflop 12 green slow")
    print("Example: drip full blue fast")

    print("\nEFFECTS")
    for effect_cmd in ValidEffects:
        print("   ", effect_cmd)

    print("\nCOMPOSITORS")
    for c in ValidCompositors:
        print("   ", c)

    print("\nCOLORS")
    for c in ValidColors.keys():
        print("   ", c)

    print("OPTIONS")
    for opt in ValidSpeeds:
        print("   ", opt)
