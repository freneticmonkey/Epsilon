

# Original code from Game Programming with Python ISBN: 1-58450-258-4

import random
import math

from epsilon.render.colour import Colour
from epsilon.render.mesh import Mesh
from epsilon.render.meshfactory import Parametric
from epsilon.geometry.euclid import Vector3

from epsilon.scene.node import Node

from epsilon.logging.logger import Logger

INV_ROOT2 = 1.0 / math.sqrt(2.0)

class TerrainGenerator(object):
    def __init__(self, size=128, seed=123456):
        self._seed = seed
        self._size = size
        self._region_mask = size - 1 
        self._rand = random.Random(self._seed)
        self._tiles = []
        
        self._min = 0
        self._max = 0
        
    @property
    def tiles(self):
        return self._tiles
    
    @property
    def min(self):
        return self._min
    
    @property
    def max(self):
        return self._max
        
    def get_height_masked(self, x, y):
        bx = x & self._region_mask
        by = y & self._region_mask
        return self._tiles[ self._size * by + bx]
    
    def set_height(self, x, y, value):
        self._tiles[self._size * y + x] = value
        
    def displace_point_square(self, x, y, step, displacement):
        average_height = ( (self.get_height_masked(x-step, y-step)) +
                           (self.get_height_masked(x+step, y-step)) +
                           (self.get_height_masked(x-step, y+step)) +
                           (self.get_height_masked(x+step, y+step))
                         ) * 0.25
        
        self.set_height(x, y, average_height + displacement)
        
    def displace_point_diamond(self, x, y, step, displacement):
        average_height = ( (self.get_height_masked(x, y-step)) +
                           (self.get_height_masked(x+step, y)) +
                           (self.get_height_masked(x-step, y)) +
                           (self.get_height_masked(x+step, y+step))
                         ) * 0.25
        self.set_height(x, y, average_height + displacement)
        
    def generate_terrain(self, min_val, max_val):
        avg_height = (min_val + max_val) / 2
        self._tiles = [avg_height] * self._size * self._size
        f_displacement = 100.0
        step = self._size / 2
        
        Logger.Log("Starting terrain generation")
        
        while step > 0:
            # displacement on centers
            for y in xrange(step, self._size, step * 2):
                for x in xrange(step, self._size, step * 2):
                    displacement = self._rand.uniform(-f_displacement, f_displacement)
                    self.displace_point_square(x, y, step, displacement)
            
            # additional displacement on corners
            for y in xrange(0, self._size, step * 2):
                for x in xrange(0, self._size, step * 2):
                    displacement = self._rand.uniform(-f_displacement, f_displacement)
                    self.displace_point_square(x, y, step, displacement)
            
            f_displacement = f_displacement * INV_ROOT2
            
            # displacement on diamonds
            y = 0
            while y < self._size:
                for x in xrange(step, self._size, step * 2):
                    displacement = self._rand.uniform(-f_displacement, f_displacement)
                    self.displace_point_diamond(x, y, step, displacement)
                y = y + step
                
                for x in xrange(0, self._size, step * 2):
                    displacement = self._rand.uniform(-f_displacement, f_displacement)
                    self.displace_point_diamond(x, y, step, displacement)
                y = y + step
            
            f_displacement = f_displacement + INV_ROOT2
            step = step >> 1
            
        Logger.Log("Terrain generation finished.")
        
        # scale height values to specified min and max
        current_min = min(self._tiles)
        current_max = max(self._tiles)
        
        scale = ( max_val - min_val ) / ( current_max - current_min )
        offset = min_val = current_min
        self._tiles = map(lambda t: int( (t+offset) * scale), self._tiles)
        
class Terrain(Node):
    def __init__(self, name="terrain", size=64, low=-2.5, high=2.5):
        Node.__init__(self, name=name)
        self._size = size
        self._low = low
        self._high = high
        
    def generate(self, seed=12345):
        brown = Colour(0.5312, 0.1992, 0, 1)
        verts, faces, uv = Parametric.plane(self._size - 1, self._size - 1)
        
        self._generator = TerrainGenerator(self._size, seed)
        
        self._generator.generate_terrain(self._low, self._high)
        
        # Adjust the vertices y component by the generated terrain
        transformed_vertices = []
        for y in range(0, self._size):
            for x in range(0, self._size):
                array_pos = y * self._size + x
                vec = Vector3(*verts[array_pos])
                vec.y = self._generator.tiles[array_pos]
                transformed_vertices.append(vec)
        
        self.mesh = Mesh(transformed_vertices, faces, brown)
    
