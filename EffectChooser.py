"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076
https://github.com/FRC1076
"""
from NeoConfig import *
from DemoCommands import ValidEffects,ValidDivisions,ValidCompositors,ValidColors,ValidSpeeds,TAP,NO_TAP,show_help
from LightingEffects import RunnerEffect, FlipFlopEffect, WipeFillEffect, SqueezeFillEffect, BlinkyEffect
from LightingEffects import DripEffect, RainbowEffect, SoundMeterEffect, GradientEffect
from ControlEffects import WaitEffect

class EffectChooser:
    """

    """
    def __init__(self, pixel_buffer=None, pixel_buffer_list=None):
        """
        Usually pass in a pixel_buffer, but when there are multiple buffers to be combined by the Compositor,
        there will be a list of buffers that could be passed to the effect.    Can specify only 1 or a list.
        Not both.
        """
        assert pixel_buffer is None or pixel_buffer_list is None, "Specify buffer or buffer_list, not both"
        self._pixel_buffer = pixel_buffer
        self._pixel_buffer_list = pixel_buffer_list
        pass

    def get_effect_name(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[0]
        except:
            name = None
        return name

    def get_effect_comp_name(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[1]
        except:
            name = None
        return name

    def get_effect_color(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[2]
            color = ValidColors[name]
        except:
            color = PURPLE
        return color

    def get_effect_speed(self, effect_cmd):
        try:
            name = effect_cmd.split(' ')[3]
            speed = ValidSpeeds[name]
        except:
            speed = 1
        return speed

    def get_chosen_effects(self, effect_cmd):
        """
        Return a list of effects to run simultaneously.
        """
        if effect_cmd == "help":
            show_help()

        topo_comps = [ "full", "oval", "digitH", "digitV", "digitS" ]

        if self._pixel_buffer_list is not None:
            print("get_chosen_effects: len(buffer_list):", len(self._pixel_buffer_list))
        if self._pixel_buffer is not None:
            print("get_chosen_effects: len(buffer:", len(self._pixel_buffer))
        effect_name = self.get_effect_name(effect_cmd)
        comp_name = self.get_effect_comp_name(effect_cmd)
        color = self.get_effect_color(effect_cmd)
        speed = self.get_effect_speed(effect_cmd)
        print("Name:", effect_name, "Comp:", comp_name, "Color:", color, "Speed:", speed)

        if effect_name == "wipe" and comp_name in topo_comps:
            return [ WipeFillEffect(self._pixel_buffer, color=color, slowness=speed), WaitEffect(self._pixel_buffer, slowness=speed) ]
        elif effect_name == "Wait" and comp_name == "full":
            return [ WaitEffect(self._pixel_buffer, color=color, slowness=speed) ]
        elif effect_name == "flipflop":
            div_names = ValidDivisions
            if comp_name in topo_comps:
                return [ FlipFlopEffect(self._pixel_buffer, color=color, slowness=speed) ]
            elif comp_name in div_names:
                divs = int(comp_name)
                return [ FlipFlopEffect(self._pixel_buffer_list[i], color=color, slowness=speed, name="FlipFlop"+str(i)) for i in range(divs) ]
        elif effect_name == "squeeze":
            div_names = ValidDivisions
            if comp_name in topo_comps:
                return [ SqueezeFillEffect(self._pixel_buffer, color=color, slowness=speed) ]
            elif comp_name in div_names:
                divs = int(comp_name)
                return [ SqueezeFillEffect(self._pixel_buffer_list[i], color=color, slowness=speed) for i in range(divs) ]

        elif effect_name == "sound":
            if comp_name in topo_comps:
                return [ SoundMeterEffect(self._pixel_buffer, color=color, slowness=speed) ]
            elif comp_name in ValidDivisions:
                divs = int(comp_name)
                return [ SoundMeterEffect(self._pixel_buffer_list[i], color=color, slowness=speed) for i in range(divs) ]

        elif effect_name == "clear" and comp_name == "all":
            return [ WipeFillEffect(self._pixel_buffer, color=OFF, slowness=1) ]
        elif effect_name == "clap" and comp_name == "full":
            return [ ClapEffect(self._pixel_buffer, color=color, slowness=speed) ]
        elif effect_name == "multi" and comp_name == "4":
            return [ RainbowEffect(self._pixel_buffer_list[0], slowness=5),
                     RunnerEffect(self._pixel_buffer_list[1], color=color, slowness=speed),
                     WipeFillEffect(self._pixel_buffer_list[2], color=BUTTERSCOTCH, slowness=5),
                     FlipFlopEffect(self._pixel_buffer_list[3], color=RED, slowness=25) ]
        elif effect_name == "multi" and comp_name == "12":
            return [ RainbowEffect(self._pixel_buffer_list[0], slowness=5),
                     RunnerEffect(self._pixel_buffer_list[1], color=color, slowness=speed),
                     WipeFillEffect(self._pixel_buffer_list[2], color=BUTTERSCOTCH, slowness=5),
                     FlipFlopEffect(self._pixel_buffer_list[3], color=RED, slowness=25),
                     RainbowEffect(self._pixel_buffer_list[4], slowness=5),
                     RunnerEffect(self._pixel_buffer_list[5], color=color, slowness=speed),
                     WipeFillEffect(self._pixel_buffer_list[6], color=BUTTERSCOTCH, slowness=5),
                     FlipFlopEffect(self._pixel_buffer_list[7], color=RED, slowness=25),
                     RainbowEffect(self._pixel_buffer_list[8], slowness=5),
                     RunnerEffect(self._pixel_buffer_list[9], color=color, slowness=speed),
                     WipeFillEffect(self._pixel_buffer_list[10], color=BUTTERSCOTCH, slowness=5),
                     FlipFlopEffect(self._pixel_buffer_list[11], color=RED, slowness=25) ]
        elif effect_name == "rainbow":
            if comp_name in topo_comps:
                return [ RainbowEffect(self._pixel_buffer, slowness=10) ]
            elif comp_name in ValidDivisions:
                divs = int(comp_name)
                return [ RainbowEffect(self._pixel_buffer_list[i], slowness=speed) for i in range(divs) ]
        elif effect_name == "runner":
            div_names = ValidDivisions
            if comp_name in topo_comps:
                return [ RunnerEffect(self._pixel_buffer, color=color, slowness=speed) ]
            elif comp_name in div_names:
                divs = int(comp_name)
                return [ RunnerEffect(self._pixel_buffer_list[i], color=color, slowness=speed) for i in range(divs) ]
        elif effect_name == "drip":
            if comp_name in topo_comps:
                """
                KLUDGE ALERT: borrow the speed part of the command to enable tap on drip
                """
                return [ DripEffect(self._pixel_buffer, slowness=1, tap=speed) ]
            elif comp_name in ValidDivisions:
                divs = int(comp_name)
                return [ DripEffect(self._pixel_buffer_list[i], slowness=1, tap=speed) for i in range(divs) ]
        elif effect_name == "fliprunner":
            # this does not work until we have a more powerful compositor
            if comp_name == "frameNcorners":
                re = [ RunnerEffect(self._pixel_buffer_list[5], color=color, slowness=speed) ]
                return re + [ FlipFlopEffect(self._pixel_buffer_list[i], color=red, slowness=speed) for i in range(4) ]
        elif effect_name == "gradient":
            if comp_name in topo_comps:
                # Kind of a KLUDGE here
                # Run this along with a Wait effect to keep it displayed for a bit
                return [ GradientEffect(self._pixel_buffer, color=color,), WaitEffect(self._pixel_buffer, slowness=speed) ]
            elif comp_name in ValidDivisions:
                divs = int(comp_name)
                ges = [ GradientEffect(self._pixel_buffer_list[i], color=color,) for i in range(divs) ]
                we = [ WaitEffect(self._pixel_buffer, slowness=speed) ]
                return ges + we

        else:
            print(f"Command [{effect_cmd}] matches nothing.  Just gonna do a purple wipe")
            return [ WipeFillEffect(self._pixel_buffer, color=PURPLE, slowness=1) ]

