class Particle:
    def __init(self, s=[0,0], v=[0,0]):
        self._s=s
        self._v=v
        return self

class Physics:  
    def __init__(self, time=0, g=(0.1,0), interval=0.02):
        """
        
        """
        self._t0=time
        self._time=time
        self._interval=interval
        self._particles=[]
        half_t_squared = self._interval*self._interval / 2
        self.half_gt_squared=(g(0)*t_squared, g(1)*t_squared)
        return self

    def add_particle(self, particle):
        self._particles.add(particle)

    def remove_a_particle(self):
        return self._particles.pop()

    def update_a_particle(self, p):
        for d in (0,1):
            p._s[d] = p._s[d] + p._v[d]*self._interval + self._half_gt_squared(d)
        
    def update_world(self):
        for p in self._particles:
            self._time += self._interval
            self.update_a_particle(p)

    def dump(self):
        for p in self._particles:
            print(format("%f.2, %f.2", p._s[0], p._s[1]))
          
          
        
      
        
    
