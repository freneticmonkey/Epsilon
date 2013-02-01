import threading

from multiprocessing import Process

from noise import _simplex, _perlin



class NoiseThread(threading.Thread):
	"""Threaded Perlin Noise"""
	def __init__(self, size, pos, x_start, x_end):
	  threading.Thread.__init__(self)
	  self._size = size
	  self._x_start = x_start
	  self._x_end = x_end
	  self._pos = pos

	  self._perlin_data = []

	def get_position(self):
		return self._pos

	def get_noise(self):
		return self._perlin_data

	def run(self):
	  
	 #  	perlin = Perlin(12345)
		# frac = FractalNoise(h=1.0, lacunarity=50.0, octaves=4.2, noise=perlin )

		self._perlin_data = []

		z = 0.5

		octaves = 6

		scale = 2 * octaves

		ls3 = 10 * octaves

		ls2 = 15 * octaves

		ls = 20 * octaves

		for x in range(self._x_start, self._x_end):
		  for y in xrange(self._size):
		    value = _perlin.noise3(float(x) / ls, float(y) / ls, z, octaves, 0.5)#, base=0)

		    if value > 0.8 or value < 0:
		      value = -1
		    else:
		      value += _perlin.noise3(float(x) / scale, float(y) / scale, z, octaves, 0.5)#, base=0)
		  
		      value += _perlin.noise3(float(x) / ls2, float(y) / ls2, z, octaves, 0.5)#, base=0)

		      value += _perlin.noise3(float(x) / ls3, float(y) / ls3, z, octaves, 0.5)#, base=0)
			
		    value = value * 127.0 + 128.0
		    self._perlin_data += [value, value, value, 1.0] 


# class NoiseProcess(Process):
# 	"""Perlin Noise Process"""
# 	def __init__(self, size, pos, x_start, x_end):
# 	  Process.__init__(self)
# 	  self._size = size
# 	  self._x_start = x_start
# 	  self._x_end = x_end
# 	  self._pos = pos

# 	  self._perlin_data = []

# 	def get_position(self):
# 		return self._pos

# 	def get_noise(self):
# 		return self._perlin_data

# 	def run(self):
# 		self._perlin_data = []
# 		z = 0.5
# 		octaves = 6
# 		scale = 2 * octaves
# 		ls3 = 10 * octaves
# 		ls2 = 15 * octaves
# 		ls = 20 * octaves

# 		for x in range(self._x_start, self._x_end):
# 		  for y in xrange(self._size):
# 		  	value = _perlin.noise3(float(x) / ls, float(y) / ls, z, octaves, 0.5)#, base=0)

# 		    if value > 0.8 or value < 0:
# 		      value = -1
# 		    else:
# 		      value += _perlin.noise3(float(x) / scale, float(y) / scale, z, octaves, 0.5)#, base=0)
# 		      value += _perlin.noise3(float(x) / ls2, float(y) / ls2, z, octaves, 0.5)#, base=0)
# 		      value += _perlin.noise3(float(x) / ls3, float(y) / ls3, z, octaves, 0.5)#, base=0)
# 		    value = value * 127.0 + 128.0
# 		    self._perlin_data += [value, value, value, 1.0]

def process_image_section(out_queue, size, pos, x_start, x_end):
    perlin_data = []
    z = 0.5
    octaves = 6
    scale = 2 * octaves
    ls3 = 10 * octaves
    ls2 = 15 * octaves
    ls = 20 * octaves

    for x in range(x_start, x_end):
      for y in xrange(size):
        value = _perlin.noise3(float(x) / ls, float(y) / ls, z, octaves, 0.5)#, base=0)

        if value > 0.8 or value < 0:
          value = -1
        else:
          value += _perlin.noise3(float(x) / scale, float(y) / scale, z, octaves, 0.5)#, base=0)
          value += _perlin.noise3(float(x) / ls2, float(y) / ls2, z, octaves, 0.5)#, base=0)
          value += _perlin.noise3(float(x) / ls3, float(y) / ls3, z, octaves, 0.5)#, base=0)
        value = value * 127.0 + 128.0
        perlin_data += [value, value, value, 1.0] 

    out_queue.put([pos, perlin_data] )

    def process_image_section(out_queue, pr):

        perlin_data = []
        octaves = 6.0
        scale = 2 * octaves
        ls3 = 10 * octaves
        ls2 = 15 * octaves
        ls = 20 * octaves

        # If the FRONT or BACK
        if pr.face == 4 or pr.face == 1:
            z = pr.zstart
            x_start = pr.x_start
            x_end = pr.x_end
            y_end = pr.y_end

            for x in range(x_start, x_end):
              for y in xrange(y_end):

                value = _perlin.noise3(x / ls, y / ls, z / ls, octaves, 0.5)#, base=0)

                if value > 0.8 or value < 0:
                  value = -1
                else:
                  value += _perlin.noise3(x / scale, y / scale, z / scale, octaves, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls2, y / ls2, z / ls2, octaves, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls3, y / ls3, z / ls2, octaves, 0.5)#, base=0)

                value = value * 127.0 + 128.0
                perlin_data += [value, value, value, 1.0] 

        # if the TOP or BOTTOM
        elif pr.face == 0 or pr.face == 3:
            y = pr.ystart

            x_start = pr.x_start
            x_end = pr.x_end
            z_end = pr.z_end

            for x in range(x_start, x_end):
              for z in xrange(z_end):

                value = _perlin.noise3(x / ls, y / ls, z, octaves, 0.5)#, base=0)

                if value > 0.8 or value < 0:
                  value = -1
                else:
                  value += _perlin.noise3(x / scale, y / scale, z / scale, octaves, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls2, y / ls2, z / ls2, octaves, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls3, y / ls3, z / ls3, octaves, 0.5)#, base=0)

                value = value * 127.0 + 128.0
                perlin_data += [value, value, value, 1.0]


        # if the RIGHT or LEFT
        elif pr.face == 2 or pr.face == 5:
            x = pr.xstart

            y_end  = pr.y_end
            z_start = pr.z_start
            z_end = pr.z_end

            for z in range(z_start, z_end):
              for y in xrange(y_end):

                value = _perlin.noise3(x / ls, y / ls, z, octaves, 0.5)#, base=0)

                if value > 0.8 or value < 0:
                  value = -1
                else:
                  value += _perlin.noise3(x / scale, y / scale, z / scale, octaves, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls2, y / ls2, z / ls2, octaves, 0.5)#, base=0)
                  value += _perlin.noise3(x / ls3, y / ls3, z / ls3, octaves, 0.5)#, base=0)

                value = value * 127.0 + 128.0
                perlin_data += [value, value, value, 1.0]
                
        out_queue.put([face, pos, perlin_data] )
