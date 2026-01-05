class Particle:    
    def __init__(self, s, v):
        """
        Every particle has a vector position and velocity
        """
        self._s=s
        self._v=v
        return

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


        
      
        
    
