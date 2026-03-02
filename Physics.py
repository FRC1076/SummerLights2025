"""
SPDX-License-Identifier: BSD-3-Clause
Copyright 2025-2026 Pioneer Robotics: PiHi Samurai, FRC Team 1076 
https://github.com/FRC1076

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
class Particle:
    def __init__(self, s, v):
        """
        Every particle has a vector position and velocity
        """
        self._s=s
        self._v=v
        return

    def index(self):
        """
        Trivial map from y axis position to linear pixel index
        """
        return round(self._s[1])

class Physics:
    def __init__(self, time=0, g=(0,-0.3), interval=0.02):
        """

        """
        self._t0=time
        self._time=time
        self._g=g
        self._interval=interval
        self._particles=[]
        return

    def add_particle(self, particle):
        self._particles.append(particle)

    def remove_a_particle(self):
        return self._particles.pop()

    def update_a_particle(self, p):
        """

        """
        for d in (0,1):
            p._s[d] = p._s[d] + p._v[d]*self._interval
            p._v[d] = p._v[d] + (self._g[d] * self._interval)

    def update_world(self):
        for p in self._particles:
            self._time += self._interval
            self.update_a_particle(p)

    def particle_indices(self, increasing=None):
        if increasing is None:
            return [ p.index() for p in self._particles ]
        else:
            return map(Particle.index, ( filter(lambda p: ((p._v[1] > 0) == increasing), self._particles) ))
            # return [ p.index() for p in self._particles if ((p._v(1) > 0) == increasing) ]

    def retire_particles(self, index_limit, speed_floor=None):
        for p in self._particles:
            if p.index() > index_limit:
                if speed_floor is None or abs(p._v[1]) < speed_floor:
                    self._particles.remove(p)

    def bounce_at_limit(self, index_limit, rebound=0.5):
        for p in self._particles:
            if p.index() > index_limit:
                p._v[1] = p._v[1] * -0.8

    def num_particles(self):
        return len(self._particles)

    def dump(self):
        for p in self._particles:
            print(f"{p._s[0]:.4f}, {p._s[1]:.4f}")



if __name__ == "__main__":


    w = Physics()
    origin = [0,0]
    up_and_to_the_right = [0.1, 0.2]
    p = Particle(origin,up_and_to_the_right)

    w.add_particle(p)

    for _ in range(68):
        w.update_world()
        w.dump()






