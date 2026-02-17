# SummerLights2025

Workspace for dynamic Neopixel animations using CircuitPython

ABOUT CIRCUITPYTHON

To run this code, you'll want a CircuitPython setup.    You'll need to download the CircuitPython image for the processor that you are using and then drag it onto the boot disk image to install it on the processor, then download the MU Editor on your laptop (which will also install some local libraries for you when it installs.
There is an additional library of the most common tools (including the NeoPixel library) that you'll need to download and then drag and drop into the "lib" directory on the processor disk image.

All the information you need is at https://circuitpython.org/

I've used the MU Editor to do development.   It is an IDE (Integrated Development Environment) a bit like the Arduino IDE (aware of the hardware -- set it up using the Mode menu! -- that is connected to your laptop via a micro-USB cable), but not as sophisticated.   For example, if you are using a Raspberry Pi Pico, you want to set the mode to "Write MicroPython Directly on Raspberry Pi Pico".   (I've not been able to get the Pico to run correctly using the CircuitPython mode in MU Editor.)

*NOTE for school laptops.    You won't be able to use the MU Editor for development.    However, if you have Chrome installed, you can use a web-based IDE to do your development.
I've tried it out, and it works pretty well.    Try it here:   https://code.circuitpython.org/*

The main way that CircuitPython operates is that it gets mounted as a disk on your laptop.   Whenever you save the code, it reruns the new version.

Note, CircuitPython is similar, but DIFFERENT than MicroPython, and the online AIs sometimes mix-up or conflate them.


ABOUT THE SOFTWARE ARCHITECTURE

I believe that we can design the software to be a bit like graphics rendering, where the different effects can be background (drawn first), or foreground (overwriting portions of the background).   Perhaps even middle ground effects are possible with the proper restrictions.     Many effects could be active at the same time, but some care will have to be taken to ensure that two foreground effects do not interfere with each other.   I think we can ensure this by requiring certain characteristics from the different effects.

Missing from this example code is some kind of triggering mechanism, but you might imagine that the effects orchestrator (the part of the software that chooses and directs the effects) might consider the current mode as well as any triggers before it picks a set of effects to run.    It could choose to ignore events until the effects were complete, or could allow them to be interrupted.

```
while The Batteries Last:

    consider the current mode/effect/trigger
    initialize the collection of effects associated with the current mode
    
    if there is static background effect, run it
    create the generators for all of the other effects

    while all of the generators are not completed:
        run each generator once

        show the rendering
        sleep for (20ms - elapsed time since last sleep)
        
        if the mode allows sensors to trigger effects:
            scan the sensors to see what relevant/compatible trigger has occurred
            break out to the outer loop if trigger is relevant
```
        
            


          

