import sys, traceback
import os

# Add the epsilon path to the python path
epsilon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(epsilon_path)

from epsilon.geometry.euclid import Vector3, Point3, Plane

p1 = Point3(0.0, 1.0, 1.0)
p2 = Point3(0.0, 0.0, 1.0)
p3 = Point3(1.0, 0.0, 0.0)

pl = Plane(p1, p2, p3)

for i in range(0,10):
	print pl._get_point()