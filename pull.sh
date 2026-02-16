# This command copies all of the files (whether or not they have been changed),
# from the CIRCUITPY disk into the current directory.    This makes it easier
# for you to make sure that all of the changes that you made on the CIRCUITPY
# disk get copied into your git development directory so you can commit and push
# the code.
#
# There are a few other ways this could be done.
# Could use the rsync command, which does comparisons based on timestamps on the
# file which could prevent you from clobbering something that you had changed
# in the development directory.
# Could maybe create your code repository *on* the CIRCUITPY disk, so you don't
# have to worry at all about copying back and forth.    My concern there is just
# whether or not the contents of the could get corrupted, as a consequence lose
# more code.   (I haven't thought about this much...)
cp /Volumes/CIRCUITPY/code.py /Volumes/CIRCUITPY/Compositor.py /Volumes/CIRCUITPY/FlipFlopEffect.py /Volumes/CIRCUITPY/LightingEffects.py /Volumes/CIRCUITPY/NeoConfig.py /Volumes/CIRCUITPY/Physics.py /Volumes/CIRCUITPY/PixelBuffer.py /Volumes/CIRCUITPY/SoundDetector.py /Volumes/CIRCUITPY/TapDetector.py /Volumes/CIRCUITPY/TestAnEffect.py .
