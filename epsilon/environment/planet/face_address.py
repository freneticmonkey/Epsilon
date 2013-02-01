#from epsilon.environment.planet.cubespheremap import CubeSphereMap
#from cubespheremap import CubeSphereMap
class CubeSphereMap(object):
    TOP =   0
    BACK =  1
    RIGHT = 2
    BOTTOM = 3
    FRONT = 4
    LEFT =  5


class FaceAddress(object):

	@staticmethod
	def get_address_bounds(address):
		face = -1

		f = address[0]

		if f == "T":
			face = CubeSphereMap.TOP
		elif f == "B":
			face = CubeSphereMap.BACK
		elif f == "R":
			face = CubeSphereMap.RIGHT
		elif f == "U":
			face = CubeSphereMap.BOTTOM
		elif f == "F":
			face = CubeSphereMap.FRONT
		elif f == "L":
			face = CubeSphereMap.LEFT

		x0 = 0.0
		y0 = 0.0
		x1 = 1.0
		y1 = 1.0

		for i in range(1, len(address)):
			c = address[i]
			width = x1 - x0
			height = y1 - y0

			if c == "A":
				# x0 / y0 are unchanged
				x1 = x0 + ( width / 2.0)
				y1 = y0 + ( height / 2.0)
			elif c == "B":
				x0 = x0 + ( width / 2.0)
				#y0 is unchanged
				#x1 is unchanged
				y1 = y0 + ( height / 2.0)
			elif c == "C":
				#x0 is unchanged
				y0 = y0 + ( height / 2.0)
				x1 = x0 + ( width / 2.0)
				#y1 is unchanged
			elif c == "D":
				x0 = x0 + ( width / 2.0)
				y0 = y0 + ( height / 2.0)

				# x0 / y0 are unchanged

		print "Address: %s converts to (%1.4f,%1.4f),(%1.4f,%1.4f)" % ( address, x0, y0, x1, y1)

		return x0, y0, x1, y1, face
	
	@staticmethod
	def get_neighbours(address):
		north = FaceAddress.get_north(address)
		south = FaceAddress.get_south(address)
		east = FaceAddress.get_east(address)
		west = FaceAddress.get_west(address)

		print "North: " + FaceAddress.get_north(address)
		print "South: " + FaceAddress.get_south(address)
		print "East: " + FaceAddress.get_east(address)
		print "West: " + FaceAddress.get_west(address)

		return north, south, east, west

	@staticmethod
	def get_north(address):
		end = address[-1]

		if end == 'A':
			address = FaceAddress.get_north(address[:-1]) + 'C'
		elif end == 'B':
			address = FaceAddress.get_north(address[:-1]) + 'D'
		elif end == 'C':
			address = address[:-1] + 'A'
		elif end == 'D':
			address = address[:-1] + 'B'

		# Faces
		elif end == "F":
			address = "T"
		elif end == "B":
			address = "T"
		elif end == "L":
			address = "T"
		elif end == "R":
			address = "T"

		elif end == "U":
			address = "F"
		elif end == "T":
			address = "B"

		return address

	@staticmethod
	def get_south(address):
		end = address[-1]

		if end == 'A':
			address = address[:-1] + 'C'
		elif end == 'B':
			address = address[:-1] + 'D'
		elif end == 'C':
			address = FaceAddress.get_south(address[:-1]) + 'A'
		elif end == 'D':
			address = FaceAddress.get_south(address[:-1]) + 'D'

		# Faces
		elif end == "F":
			address = "U"
		elif end == "B":
			address = "U"
		elif end == "L":
			address = "U"
		elif end == "R":
			address = "U"

		elif end == "U":
			address = "B"
		elif end == "T":
			address = "F"

		return address

	@staticmethod
	def get_east(address):
		end = address[-1]

		if end == 'A':
			address = address[:-1] + 'B'
		elif end == 'B':
			address = FaceAddress.get_east(address[:-1]) + 'A'
		elif end == 'C':
			address = address[:-1] + 'D'
		elif end == 'D':
			address = FaceAddress.get_east(address[:-1]) + 'C'

		# Faces
		elif end == "F":
			address = "R"
		elif end == "B":
			address = "L"
		elif end == "L":
			address = "F"
		elif end == "R":
			address = "B"

		elif end == "U":
			address = "R"
		elif end == "T":
			address = "R"

		return address

	@staticmethod
	def get_west(address):
		end = address[-1]

		if end == 'A':
			address = FaceAddress.get_west(address[:-1]) + 'B'
		elif end == 'B':			
			address = address[:-1] + 'A'
		elif end == 'C':
			address = FaceAddress.get_west(address[:-1]) + 'D'
		elif end == 'D':
			address = address[:-1] + 'C'

		# Faces
		elif end == "F":
			address = "L"
		elif end == "B":
			address = "L"
		elif end == "L":
			address = "B"
		elif end == "R":
			address = "F"

		elif end == "U":
			address = "L"
		elif end == "T":
			address = "L"

		return address

if __name__ == "__main__":
	FaceAddress.get_address_bounds("F")
	FaceAddress.get_neighbours("FBAB")


		

