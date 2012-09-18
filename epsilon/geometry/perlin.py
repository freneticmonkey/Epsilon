import random
import math

class Perlin(object):
	B = 0x100
	BM = 0xff
	N = 0x1000

	def __init__(self, seed=0):
		self._seed = seed
		self._rnd = random
		self._rnd.seed(self._seed)

		self._init_arrays()

	def _init_arrays(self):
		self._p  = [0] * (self.B + self.B + 2)
		self._g1 = [0] * (self.B + self.B + 2)
		self._g2 = [[0] * 2] * (self.B + self.B + 2)
		self._g3 = [[0] * 3] * (self.B + self.B + 2)
		
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
		self._rnd.shuffle(self._p)

		for i in range(0, self.B + 2):
			self._p[self.B + i] = self._p[i]
			self._g1[self.B + i] = self._g1[i]

			for j in range(0, 2):
				self._g2[self.B + i][j] = self._g2[i][j]

			for j in range(0, 3):
				self._g3[self.B + i][j] = self._g3[i][j]

	@staticmethod
	def normalise2(x, y):
		s = float(math.sqrt(x * x + y * y))
		return x / s, y / s

	@staticmethod
	def normalise3(x, y, z):
		s = float(math.sqrt(x * x + y * y + z * z))
		return x / s, y / s, z / s

	@staticmethod
	def s_curve(t):
		return t * t * (3.0 - (2.0 * t))

	@staticmethod
	def lerp(t, a, b):
		return a + t * (b - a)

	@staticmethod
	def at2(rx, ry, x, y):
		return rx * x + ry * y

	@staticmethod
	def at3(rx, ry, rz, x, y, z):
		return rx * x + ry * y + rz * z

	def setup(self, value):
		t = value + self.N
		b0 = int(t) & self.BM
		b1 = (b0 + 1) & self.BM
		r0 = t - int(t)
		r1 = r0 - 1.0
		return b0, b1, r0, r1

	# 1 Dimensional Noise
	def noise(self, arg):
		bx0, bx1, rx0, rx1 = self.setup(arg)
		sx = self.s_curve(rx0)
		u = rx0 * self._g1[ self._p[bx0] ]
		v = rx1 * self._g1[ self._p[bx1] ]

		print sx
		print u
		print v

		return self.lerp(sx, u, v)

	# 2 Dimensional Noise
	def noise2(self, x, y):
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
	def noise3(self, x, y, z):
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


class FractalNoise(object):

	def __init__(self, h, lacunarity, octaves, noise=None):
		self._lacunarity = lacunarity
		self._octaves = octaves
		self._i_octaves = int(octaves)
		self._exponent = []
		self._noise = None

		frequency = 1.0
		for i in range(0, self._i_octaves+1):
			self._exponent.append(math.pow(self._lacunarity, -h))
			frequency *= self._lacunarity

		if noise is None:
			self._noise = Perlin()
		else:
			self._noise = noise

	def hybrid_multi_fractal2(self, x, y, offset):

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
		signal = math.fabs(self._noise.noise3(x,y,z))
		signal = offset - signal
		signal *= signal
		result = signal
		weight = 1.0

		for i in range(1, self._i_octaves):
			x *= self._lacunarity
			y *= self._lacunarity

			weight = signal * gain
			weight = max(min(weight, 1.0), 0.0)

			signal = math.fabs(self._noise.noise3(x,y,z))
			signal = offset - signal
			signal *= signal
			signal *= weight
			result += signal * self._exponent[i]

		return result

	def brownian_motion2(self, x, y):
		value = 0.0
		for i in range(0, self._i_octaves):
			value = self._noise.noise2(x,y) * self._exponent[i]
			x *= self._lacunarity
			y *= self._lacunarity

		remainder = self._octaves - self._i_octaves
		value += remainder * self._noise.noise2(x, y) * self._exponent[self._i_octaves]

		return value

	def brownian_motion3(self, x, y, z):
		value = 0.0
		for i in range(0, self._i_octaves):
			value = self._noise.noise3(x,y,z) * self._exponent[i]
			x *= self._lacunarity
			y *= self._lacunarity

		remainder = self._octaves - self._i_octaves
		value += remainder * self._noise.noise3(x, y, z) * self._exponent[self._i_octaves]

		return value

if __name__ == "__main__":

	p = Perlin()
	f = FractalNoise(1, 2, 3, p)
	for i in range(0, 10):
		a = i * 1.234
		b = i * 2.34
		c = i * 3.123
		print "cycle: %d a: %3.2f b: %3.2f c: %3.2f" % (i, a, b, c)

		print "noise: 1: %3.3f" % p.noise(a)

		print "noise: 2: %3.3f" % p.noise2(a, b)

		print "noise: 3: %3.3f" % p.noise3(a, b, c)

		print "hybrid: %3.2f" % f.hybrid_multi_fractal2(a, b, 0.1)
		print "ridged_multi_fractal: %3.2f" % f.ridged_multi_fractal2(a,b, 0.1, 3.0)
		print "brownian_motion: %3.2f" % f.brownian_motion2(a,b)

		print "hybrid: %3.2f" % f.hybrid_multi_fractal3(a, b, c, 0.1)
		print "ridged_multi_fractal: %3.2f" % f.ridged_multi_fractal3(a,b,c, 0.1, 3.0)
		print "brownian_motion: %3.2f" % f.brownian_motion3(a,b,c)

		print "\n----------------------\n"



