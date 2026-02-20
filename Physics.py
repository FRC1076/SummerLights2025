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






