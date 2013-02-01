import random
import math
#from cython.view cimport array as cvarray
import array
from cpython cimport array

from noise import pnoise3, snoise3

cdef class Perlin(object):
	B = 0x100
	BM = 0xff
	N = 0x1000

	#cdef int ARRAY_LENGTH = B + B + 2

	cdef int _p[514]
	cdef float _g1[514]
	cdef float _g2[514][2]
	cdef float _g3[514][3]

	# _p  = cvarray(size=(ARRAY_LENGTH), itemsize=sizeof(float), format='f')
	# _g1  = cvarray(size=(ARRAY_LENGTH), itemsize=sizeof(float), format='f')
	# _g2  = cvarray(size=(ARRAY_LENGTH, 2), itemsize=sizeof(float), format='f')
	# _g3  = cvarray(size=(ARRAY_LENGTH, 3), itemsize=sizeof(float), format='f')

	# cdef float *_g1 = [ARRAY_LENGTH]
	# cdef float *_g2 = [ARRAY_LENGTH * 2]
	# cdef float *_g3 = [ARRAY_LENGTH * 3]

	# cdef float *_p  = [0] * (self.B + self.B + 2)
	# cdef float *_g1 = [0] * (self.B + self.B + 2)
	# cdef float *_g2 = [[0] * 2] * (self.B + self.B + 2)
	# cdef float *_g3 = [[0] * 3] * (self.B + self.B + 2)

	cdef int _seed
	cdef object _rnd

	def __init__(self, seed=0):
		self._seed = seed
		self._rnd = random
		self._rnd.seed(self._seed)

		self._init_arrays()

	def _init_arrays(self):
		
		cdef int i, j, k
		
		# intialise the arrays with random data
		for i in range(0, self.B):
			self._p[i] = i
			self._g1[i] = self._rnd.uniform(-1.0, 1.0)

			for j in range(0, 2):
				self._g2[i][j] = self._rnd.uniform(-1.0, 1.0)
			self._g2[i][0], self._g2[i][1] = self.normalise2(self._g2[i][0], self._g2[i][1])

			for j in range(0, 3):
				self._g3[i][j] = self._rnd.uniform(-1.0, 1.0)
			self._g3[i][0], self._g3[i][1], self._g3[i][2] = self.normalise3(self._g3[i][0], self._g3[i][1], self._g3[i][2])

		# randomly shuffle the values in the p array
		#self._rnd.shuffle(self._p)
		i = self.B
		while i != 0:
			i -= 1
			k = self._p[i]
			j = self._rnd.randint(0, self.B)
			self._p[i] = self._p[j]
			self._p[j] = k

		for i in range(0, self.B + 2):
			self._p[self.B + i] = self._p[i]
			self._g1[self.B + i] = self._g1[i]

			for j in range(0, 2):
				self._g2[self.B + i][j] = self._g2[i][j]

			for j in range(0, 3):
				self._g3[self.B + i][j] = self._g3[i][j]

	@staticmethod
	def normalise2(float x, float y):
		s = float(math.sqrt(x * x + y * y))
		return x / s, y / s

	@staticmethod
	def normalise3(float x, float y, float z):
		s = float(math.sqrt(x * x + y * y + z * z))
		return x / s, y / s, z / s

	@staticmethod
	def s_curve(float t):
		return t * t * (3.0 - (2.0 * t))

	@staticmethod
	def lerp(float t, float a, float b):
		return a + t * (b - a)

	@staticmethod
	def at2(float rx, float ry, float x, float y):
		return rx * x + ry * y

	@staticmethod
	def at3(float rx, float ry, float rz, float x, float y, float z):
		return rx * x + ry * y + rz * z

	def setup(self, float value):
		cdef int b0, b1
		cdef float r0, r1, t
		t = value + self.N
		b0 = int(t) & self.BM
		b1 = (b0 + 1) & self.BM
		r0 = t - int(t)
		r1 = r0 - 1.0
		return b0, b1, r0, r1

	# 1 Dimensional Noise
	def noise(self, float arg):
		cdef int bx0, bx1
		cdef float rx0, rx1, sx, u, v
		bx0, bx1, rx0, rx1 = self.setup(arg)
		sx = self.s_curve(rx0)
		u = rx0 * self._g1[ self._p[bx0] ]
		v = rx1 * self._g1[ self._p[bx1] ]

		return self.lerp(sx, u, v)

	# 2 Dimensional Noise
	def noise2(self, float x, float y):
		cdef:
			int bx0, bx1by0, by1
			float rx0, rx1, ry0, ry1
			float sx, sy, u, v, a, b
			int i, j, b00, b10, b01, b11

		bx0, bx1, rx0, rx1 = self.setup(x)
		by0, by1, ry0, ry1 = self.setup(y)

		i = self._p[ bx0 ]
		j = self._p[ bx1 ]

		b00 = self._p[ i + by0 ]
		b10 = self._p[ j + by0 ]
		b01 = self._p[ i + by1 ]
		b11 = self._p[ i + by1 ]

		sx = self.s_curve(rx0)
		sy = self.s_curve(ry0)

		u = self.at2(rx0, ry0, self._g2[b00][0], self._g2[b00][1] )
		v = self.at2(rx1, ry0, self._g2[b10][0], self._g2[b10][1] )
		a = self.lerp(sx, u, v)

		u = self.at2(rx0, ry1, self._g2[b01][0], self._g2[b01][1] )
		v = self.at2(rx1, ry1, self._g2[b11][0], self._g2[b11][1] )
		b = self.lerp(sx, u, v)

		return self.lerp(sy, a, b)

	# 3 Dimensional Noise
	def noise3(self, float x, float y, float z):
		cdef:
			int bx0, bx1, by0, by1, bz0, bz1
			float rx0, rx1, ry0, ry1, rz0, rz1
			float sy, sz, a, b, c, d, t, u, v
			int i, j, b00, b10, b01, b11

		bx0, bx1, rx0, rx1 = self.setup(x)
		by0, by1, ry0, ry1 = self.setup(y)
		bz0, bz1, rz0, rz1 = self.setup(z)

		i = self._p[ bx0 ]
		j = self._p[ bx1 ]

		b00 = self._p[ i + by0 ]
		b10 = self._p[ j + by0 ]
		b01 = self._p[ i + by1 ]
		b11 = self._p[ i + by1 ]

		t = self.s_curve(rx0)
		sy = self.s_curve(ry0) 
		sz = self.s_curve(rz0)

		u = self.at3(rx0,ry0,rz0, self._g3[ b00 + bz0][0], self._g3[ b00 + bz0][1], self._g3[ b00 + bz0][2])
		v = self.at3(rx1,ry0,rz0, self._g3[ b10 + bz0][0], self._g3[ b10 + bz0][1], self._g3[ b10 + bz0][2])
		a = self.lerp(t, u, v)
		
		u = self.at3(rx0,ry1,rz0, self._g3[ b01 + bz0][0], self._g3[ b01 + bz0][1], self._g3[ b01 + bz0][2])
		v = self.at3(rx1,ry1,rz0, self._g3[ b11 + bz0][0], self._g3[ b11 + bz0][1], self._g3[ b11 + bz0][2])
		b = self.lerp(t, u, v)
		
		c = self.lerp(sy, a, b)
		
		u = self.at3(rx0,ry0,rz1, self._g3[ b00 + bz1][0], self._g3[ b00 + bz1][2], self._g3[ b00 + bz1][2])
		v = self.at3(rx1,ry0,rz1, self._g3[ b10 + bz1][0], self._g3[ b10 + bz1][1], self._g3[ b10 + bz1][2])
		a = self.lerp(t, u, v)
		
		u = self.at3(rx0,ry1,rz1, self._g3[ b01 + bz1][0], self._g3[ b01 + bz1][1], self._g3[ b01 + bz1][2])
		v = self.at3(rx1,ry1,rz1, self._g3[ b11 + bz1][0], self._g3[ b11 + bz1][1], self._g3[ b11 + bz1][2])
		b = self.lerp(t, u, v)
		
		d = self.lerp(sy, a, b)
		
		return self.lerp(sz, c, d)


cdef class FractalNoise(object):
	
	cdef:
		float _lacunarity
		int _octaves
		int _i_octaves
		object _noise
		object _exponent

	def __init__(self, h, lacunarity, octaves, noise=None):
		self._lacunarity = lacunarity
		self._octaves = octaves
		self._i_octaves = int(octaves)
		#self._exponent = cvarray(shape=(octaves+1,), itemsize=sizeof(float), format='f')
		self._exponent = array.array('f', [math.pow(self._lacunarity, -h) for i in range(0, self._i_octaves+1)])
		self._noise = None

		# frequency = 1.0
		# for i in range(0, self._i_octaves+1):
		# 	self._exponent.append(math.pow(self._lacunarity, -h))
		# 	frequency *= self._lacunarity

		if noise is None:
			self._noise = Perlin()
		else:
			self._noise = noise

	def hybrid_multi_fractal2(self, x, y, offset):
		cdef int i, remainder
		cdef float weight, result
		result = (self._noise.noise2(x,y) + offset) * self._exponent[0]
		weight = result
		x *= self._lacunarity
		y *= self._lacunarity

		for i in range(1, self._i_octaves):
			if weight > 0.5:
				weight = 1.0
			signal = (self._noise.noise2(x,y) + offset) * self._exponent[i]
			result += weight * signal
			weight *= signal
			x *= self._lacunarity
			y *= self._lacunarity

		remainder = self._octaves - self._i_octaves
		result += remainder * self._noise.noise2(x,y) * self._exponent[self._i_octaves]

		return result

	def hybrid_multi_fractal3(self, x, y, z, offset):
		cdef int i
		cdef float remainder
		cdef float weight, result

		result = (self._noise.noise3(x,y,z) + offset) * self._exponent[0]
		weight = result
		x *= self._lacunarity
		y *= self._lacunarity

		for i in range(1, self._i_octaves):
			if weight > 0.5:
				weight = 1.0
			signal = (self._noise.noise3(x,y,z) + offset) * self._exponent[i]
			result += weight * signal
			weight *= signal
			x *= self._lacunarity
			y *= self._lacunarity

		remainder = self._octaves - self._i_octaves
		result += remainder * self._noise.noise3(x,y,z) * self._exponent[self._i_octaves]

		return result

	def ridged_multi_fractal2(self, x, y, offset, gain):
		cdef int i
		cdef float remainder
		cdef float weight, result

		signal = math.fabs(self._noise.noise2(x,y))
		signal = offset - signal
		signal *= signal
		result = signal
		weight = 1.0

		for i in range(1, self._i_octaves):
			x *= self._lacunarity
			y *= self._lacunarity

			weight = signal * gain
			weight = max(min(weight, 1.0), 0.0)

			signal = math.fabs(self._noise.noise2(x,y))
			signal = offset - signal
			signal *= signal
			signal *= weight
			result += signal * self._exponent[i]

		return result

	def ridged_multi_fractal3(self, x, y, z, offset, gain):
		cdef int i
		cdef float weight, result, remainder, frequency, signal

		# Get the first octave
		signal = math.fabs(pnoise3(x, y, z))
		# invert and translate ( note that the offset should be -=1.0)
		signal = offset - signal
		# square the signal to increase the sharpness of the ridges
		signal *= signal
		result = signal
		weight = 1.0

		for i in range(1, self._i_octaves):
			# increase the frequency
			x *= self._lacunarity
			y *= self._lacunarity
			z *= self._lacunarity

			# weight the successive contributions by previous signal
			weight = signal * gain
			weight = max(min(weight, 1.0), 1.0)
			signal = math.fabs(pnoise3(x, y, z))
			signal = offset - signal
			signal *= signal

			# weight the contribution
			signal *= weight
			result += signal * self._exponent[i]

		return result



		#signal = math.fabs(self._noise.noise3(x,y,z))
		# signal = math.fabs(pnoise3(x,y,z))
		# signal = offset - signal
		# signal *= signal
		# result = signal
		# weight = 1.0

		# for i in range(1, self._i_octaves):
		# 	x *= self._lacunarity
		# 	y *= self._lacunarity

		# 	weight = signal * gain
		# 	weight = max(min(weight, 1.0), 0.0)

		# 	#signal = math.fabs(self._noise.noise3(x,y,z)) 
		# 	signal = math.fabs(pnoise3(x,y,z)) 
		# 	signal = offset - signal
		# 	signal *= signal
		# 	signal *= weight
		# 	result += signal * self._exponent[i]

		return result

	def brownian_motion2(self, x, y):
		cdef int i, remainder
		cdef float weight, value

		value = 0.0
		for i in range(0, self._i_octaves):
			value = self._noise.noise2(x,y) * self._exponent[i]
			x *= self._lacunarity
			y *= self._lacunarity

		remainder = self._octaves - self._i_octaves
		value += remainder * self._noise.noise2(x, y) * self._exponent[self._i_octaves]

		return value

	def brownian_motion3(self, x, y, z):
		cdef int i, remainder
		cdef float weight, value

		value = 0.0
		for i in range(0, self._i_octaves):
			#value = self._noise.noise3(x,y,z) * self._exponent[i]
			value = math.fabs(pnoise3(x,y,z)) * self._exponent[i]
			x *= self._lacunarity
			y *= self._lacunarity

		remainder = self._octaves - self._i_octaves
		#value += remainder * self._noise.noise3(x, y, z) * self._exponent[self._i_octaves]
		value += remainder * pnoise3(x, y, z) * self._exponent[self._i_octaves]

		return value

	def turbulance3(self, x, y, z):
		cdef int i, remainder
		cdef float weight, value

		value = 0.0
		for i in range(0, self._i_octaves):
			#value = math.fabs(self._noise.noise3(x,y,z)) * self._exponent[i]
			value = math.fabs(pnoise3(x,y,z)) * self._exponent[i]
			x *= self._lacunarity
			y *= self._lacunarity

		remainder = self._octaves - self._i_octaves
		#value += remainder * math.fabs(self._noise.noise3(x, y, z)) * self._exponent[self._i_octaves]
		value += remainder * math.fabs(pnoise3(x, y, z)) * self._exponent[self._i_octaves]
		return value
def test():
	p = Perlin()
	f = FractalNoise(1, 2, 3, p)
	# for i in range(0, 100):
	# 	a = i * 1.234
	# 	b = i * 2.34
	# 	c = i * 3.123
	for x in range(32):
		for y in range(32):
			x /= 32.0
			y /= 32.0
			z = 0.3
		# print "cycle: %d a: %3.2f b: %3.2f c: %3.2f" % (i, a, b, c)
		# print ">> noise: 1: %3.3f" % p.noise(a)

		# print "noise: 2: %3.3f" % p.noise2(a, b)

			print "noise: 3: %3.3f" % p.noise3(x, y, z)

		# print "hybrid multi fractal 2: %3.2f" % f.hybrid_multi_fractal2(a, b, 0.1)
		# print "hybrid multi fractal 3: %3.2f" % f.hybrid_multi_fractal3(a, b, c, 0.1)

		# print "ridged multi fractal 2: %3.2f" % f.ridged_multi_fractal2(a,b, 0.1, 3.0)
		# print "ridged multi fractal 3: %3.2f" % f.ridged_multi_fractal3(a,b,c, 0.1, 3.0)

		# print "brownian motion 2: %3.2f" % f.brownian_motion2(a,b)
		# print "brownian motion 3: %3.2f" % f.brownian_motion3(a,b,c)

		print "\n----------------------\n"

if __name__ == "__main__":
	test()



