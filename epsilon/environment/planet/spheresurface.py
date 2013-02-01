from datetime import datetime
import numpy

#PyOpenGL types
#from epsilon.render.meshfactory import *
from OpenGL.GL import *
from OpenGL.GLU import *

matrix_type = GLfloat * 16
matrix_typed = GLdouble * 16

from epsilon.render.mesh import Mesh
from epsilon.render.colour import Preset

from epsilon.geometry.perlin import Perlin, FractalNoise
from noise import _perlin

from epsilon.render.texture import GeneratedTexture
from epsilon.render.texturemanager import TextureManager

from epsilon.environment.planet.cubespheremap import CubeSphereMap

from epsilon.geometry.euclid import Vector3

class SphereSurface(object):
    
    # parameters are the bounds of the region in which the sphere surface needs to 
    # be generated 
    def __init__(self, increments=10, radius=1.0, max_height=None):
        self._increments = increments
        
        self._radius = radius

        self._generated_meshes = {}
        self._generated_noise = {}
        self._generated_textures = {}

        self._max_height = max_height


        self._seed = 123456
        self._h = 1.0
        self._lacunarity = 2.0
        self._octaves = 4.2
        self._noise = FractalNoise(self._h, self._lacunarity, self._octaves, Perlin(self._seed))

    def _get_noise(self, pos):
        # noise
        x = pos.x
        y = pos.y
        z = pos.z

        #first_scale = 8 * self._octaves

        # h = self._planet_root.max_height * self._planet_root.noise.ridged_multi_fractal3(p.x, p.y, p.z, 0.0, 1.0)
        
        #frac = self._noise.ridged_multi_fractal3(x / first_scale, y / first_scale, z / first_scale, -0.1, 1.0)
        #frac += self._noise.turbulance3(x / first_scale, y / first_scale, z / first_scale)

        # data.append( perlin.noise3( v.x, v.y, v.z) * 255.0 )
        # data.append( self._noise.brownian_motion3( v.x, v.y, v.z) * 255.0 )
        # data.append( ( (self._noise.ridged_multi_fractal3(v.x, v.y, v.z, -0.1, 1.0) + 1.0) / 2.0) * 255.0 )

        # frac = self._noise.ridged_multi_fractal3(v.x / first_scale, v.y / first_scale, v.z / first_scale, -0.1, 1.0)
        
        # frac += self._noise.turbulance3(v.x / first_scale, v.y / first_scale, v.z / first_scale)
        
        #frac = pnoise3(v.x / first_scale, v.y / first_scale, v.z / first_scale)#, octaves=4)
        #frac += pnoise3(v.x / second_scale, v.y / second_scale, v.z / second_scale)#, octaves=4 )

        #frac += pnoise3(v.x / second_scale, v.y / second_scale, v.z / second_scale, octaves=4 )

        #height = ( frac * 127.0 ) + 128.0

        octaves = 6.0

        ioct = int(octaves)
        scale = 2 * octaves
        ls3 = 10 * octaves
        ls2 = 15 * octaves
        ls = 20 * octaves

        value = _perlin.noise3(x / ls, y / ls, z / ls, ioct, 0.5)#, base=0)

        if value > 0.8 or value < 0:
          value = -1
        # else:
        # if value < -0.8:
        #   value = -1
        else:
          value += _perlin.noise3(x / scale, y / scale, z / scale, ioct, 0.5)#, base=0)      
          value += _perlin.noise3(x / ls2,   y / ls2,   z / ls2,   ioct, 0.5)#, base=0)
          value += _perlin.noise3(x / ls3,   y / ls3,   z / ls3,   ioct, 0.5)#, base=0)
        
        frac = value
        #print frac
        return frac
    
    def _gen_verts(self, address):
        bound_min_x, bound_min_z, bound_max_x, bound_max_z, face = CubeSphereMap.get_address_bounds(address)

        verts = []
        noise_x = []

        h_height = self._max_height / 2.0

        for i in xrange(self._increments + 1):
            #c = i * (1.0 / self._increments)
            c = (i * ( (bound_max_x - bound_min_x) / float(self._increments) ) ) + bound_min_x
            nv = []

            noise_y = []
            for j in xrange(self._increments + 1):
                #r = j * ( 1.0 / self._increments )
                r = (j * ( (bound_max_z - bound_min_z) / float(self._increments) ) ) + bound_min_z
                
                p = CubeSphereMap.get_sphere_vector(c, r, face) * self._radius
                
                n = Vector3()#c, r, -1) * self._radius
                if True:
                
                    u = c
                    v = r
                    u = (u * 2.0) - 1.0
                    v = (v * 2.0) - 1.0
                    if face == CubeSphereMap.BACK:
                        n = Vector3(-u, -v, -1) * self._radius
                    elif face == CubeSphereMap.LEFT:
                        n = Vector3(-1, -v, u) * self._radius
                    elif face == CubeSphereMap.RIGHT:
                        n = Vector3(1, -v, -u) * self._radius
                    elif face == CubeSphereMap.TOP:
                        n = Vector3(u, 1, v) * self._radius
                    elif face == CubeSphereMap.BOTTOM:
                        n = Vector3(u, -1, -v) * self._radius
                    elif face == CubeSphereMap.FRONT:
                        n = Vector3(u, -v, 1) * self._radius
                else:
                # Adjust the surface level using noise
                    n = p.copy()

                # if face == CubeSphereMap.RIGHT:
                #     n.x = self._radius
                # elif face == CubeSphereMap.LEFT:
                #     n.x = -self._radius
                # elif face == CubeSphereMap.TOP:
                #     n.y = self._radius
                # elif face == CubeSphereMap.BOTTOM:
                #     n.y = -self._radius
                # elif face == CubeSphereMap.FRONT:
                #     n.z = self._radius
                # elif face == CubeSphereMap.BACK:
                #     n.z = -self._radius

                frac = self._get_noise(n)
                
                # if i == 0 and j == 0:
                #     frac = 5.0
                # if i == self._increments and j == self._increments:
                #     frac = 10.0

                # if j in [4, 6, 8, 20, 25, 30]:
                #     frac = 1
                # else:
                #     frac = -1

                # if i in [5,6,20,21]:
                #     frac = 1

                #noise.append(frac)
                noise_y.append(frac)

                nv.append(frac)
                #h = noise * self._max_height
                h = (frac * h_height ) + h_height
                
                # Increase the surface vector by the noise value
                n = p.normalized()
                n *= h

                p += n

                verts.append((p.x, p.y, p.z))
            # s = ""
            # for n in nv:
            #     s += "\t%0.3f," % n
            # print s
            noise_x.append(noise_y)
        return verts, noise_x

    # def gen_mesh(self, bound_min_x=0.0, 
    #                    bound_max_x=1.0, 
    #                    bound_min_z=0.0, 
    #                    bound_max_z=1.0,
    #                    face=CubeSphereMap.TOP):
    def gen_mesh(self, address):
        mesh = None

        if address in self._generated_meshes:
            mesh = self._generated_meshes[address]

        else:

            #b = datetime.now()

            bound_min_x, bound_min_z, bound_max_x, bound_max_z, face = CubeSphereMap.get_address_bounds(address)

            verts, noise = self._gen_verts(address)
                    
            faces = []
            v = 0
            for c in xrange(self._increments):
                for r in xrange(self._increments):
                    bl = v + c + r
                    tl = bl + 1
                    tr = tl + self._increments + 1
                    br = tr - 1
                    
                    faces.append((bl, tl, tr))
                    faces.append((bl, tr, br))
                v = v + self._increments
            
            tex_coords = []
            
            bound_width = bound_max_x - bound_min_x
            bound_height = bound_max_z - bound_min_z

            for i in xrange(self._increments + 1):
                # Generate 0.0 - 1.0 local uv coords
                c = i * (1.0 / (self._increments))

                # generate global uv coords i.e. 0.2 - 0.3
                #c = (i * (bound_width / float(self._increments) ) ) + bound_min_x
                tc = []

                for j in xrange(self._increments + 1):
                    # local
                    r = j * ( 1.0 / (self._increments))
                    
                    # global
                    #r = (j * ( bound_height / float(self._increments) ) )+ bound_min_z
                    
                    #y = j/self._increments
                    p = [c,r] 
                    tex_coords.append(p)
                    tc.append(p)

                # s = ""
                # for n in tc:
                #     s += "\t(%0.3f,%0.3f)," % (n[0], n[1])
                # print s
            #print "%s Vertex gen time: %3.5f" % (address, (datetime.now() - b).total_seconds())

            b = datetime.now()

            # Build a mesh
            mesh = Mesh(verts, faces, Preset.green, tex_coords=tex_coords)
            self._generated_meshes[address] = mesh
            self._generated_noise[address] = noise

            print "%s Mesh obj Gen time: %3.5f" % (address, (datetime.now() - b).total_seconds())
        
        return mesh

    def _gen_texture(self, address, resolution=None):
        texture_name = None

        # If the a texture for the address has already been generated
        if address in self._generated_textures:
            texture_name = self._generated_textures[address]

        # Otherwise generate a new texture
        else:

            face = CubeSphereMap.get_address_face(address)
            level = len(address)

            name = "planet_texture"
            size = self._increments #256

            if not resolution is None:
                size = resolution

            data = None
            format_size = 4
            pitch = size * format_size
            format = "RGBA"

            #b = datetime.now()

            # Generate the data for the texture
            
            #perlin = Perlin(12345)

            # Generate sphere coordinates for the address
            # verts = []
            # for x in range(size):
            #     o = ""
            #     x /= float(size)

            #     for y in range(size):
            #         y /= float(size)
            #         # verts.append( Vector3(x, y, 0.5) )
            #         coord = CubeSphereMap.get_sphere_vector(x, y, face) * self._radius
            #         # #print coord
            #         verts.append( coord )

            #         o += " (%1.2f, %1.2f)" % (x, y)
            #verts = self._gen_verts(address)
            # mesh = self._generated_meshes[address]
            # verts = mesh.vertices
                
                #print o

            #ignoring faces
            #print verts
            # as image data is loaded from bottom-left to top-right vertex data
            # needs to be transformed as it is generated top-left to bottom-right

            # t_data = []
            # for x in xrange(size-1, -1, -1):
            #     row_start = x * size
            #     row_end = row_start + size
            #     t_data += verts[row_start:row_end]

            # for x in range(size):
            #     row_start = x * size
            #     row_end = row_start + size

                # o = ""
                # for v in verts[row_start:row_end]:
                #     o += " (%1.2f, %1.2f, %1.2f)" % (v.x, v.y, v.z)

            # Generate noise
            #data = [self._noise.ridged_multi_fractal3(v[0], v[1], v[2], 0, 1.0) for v in t_data]
            #data = [self._noise.ridged_multi_fractal3(v[0], v[1], v[2], 0, 1.0) for v in t_data]
            
            # data = [perlin.noise3(v.x, v.x, v.x) * 255.0 for v in verts]

            # first_scale = 8 * self._octaves

            #second_scale = 0.5 * self._octaves
            
            # data = []

            noise = self._generated_noise[address]

            # t_data = []
            # for x in xrange(size-1, -1, -1):
            #     row_start = x * size
            #     row_end = row_start + size
            #     t_data += noise[row_start:row_end]

            # for x in range(size):
            #     row_start = x * size
            #     row_end = row_start + size

            # noise = t_data

            colour_data = []

            #for v in verts:
            # for n in noise:
            for y in range(self._increments):#,-1,-1):
                nv = []
                for x in range(self._increments):#,-1,-1):

                    n = noise[x][y]
                    # # convert the height to a colour value
                    # #height = ( (v.magnitude() - self._radius) / self._max_height ) * 255.0

                    #nv.append(n)

                    # if n > 1.0:
                    #     print "n: %3.2f x: %d y: %d" % ( n, x, y)

                    height = (n * 128.0) + 128.0

                    # #height = 150.0
                    # #print height

                    colour = Preset.white

                    if 200 >= height >= 150:
                        colour = Preset.green
                    elif 150 > height > 100:
                        colour = Preset.yellow
                    elif 100 >= height:
                        colour = Preset.blue
                    
                    # if 50 > height:
                    #     colour = Preset.blue
                    # else:
                    #     colour = Preset.red

                    # if x == 0 or x == self._increments-1:
                    #     colour = Preset.yellow

                    # if y == 0 or y == self._increments-1:
                    #     colour = Preset.green
                    
                    # colour = Preset.red

                    # colour = colour.tinted(Preset.green, (y/float(size)))
                    # colour = colour.tinted(Preset.blue, (x/float(size)))

                    colour_data += [colour.r * 255.0, colour.g * 255.0, colour.b * 255.0, colour.a * 255.0]
                # s = ""
                # for n in noise[x]:
                #     s += "\t%0.3f," % n
                # print s

            #e = datetime.now() - b

            #print "%s Tex Colours Gen time: %3.5f" % (address, e.total_seconds())#(e.seconds +  (e.microseconds / 1000000.0) ) )

            # colour_data = []
            # for n in noise:
            
            #     nv.append(n)

            #     height = (n * 128.0) + 128.0

            #     if 100 > height:
            #         colour = Preset.blue
            #     else:
            #         colour = Preset.red

            #     colour_data += [colour.r * 255.0, colour.g * 255.0, colour.b * 255.0, colour.a * 255.0]

            #b = datetime.now()

            # Transform noise to colour data
            array_data = numpy.array(colour_data, 'f')

            # array_data = numpy.random.random_integers(low=0,
            #                                           high=255,
            #                                           size = (size * size, format_size))

            #array_data *= 255
            # array_data[:,3] = 255
            array_data.shape = -1
            tex_data = (GLubyte * array_data.size)(*array_data.astype('u1'))

            #test_plane = SceneManager.get_instance().current_scene.root.transform.get_child_with_name("test_plane")

            texture_name = "planet_texture_%s" % address
            
            new_planet_texture = GeneratedTexture(name=texture_name, width=size, height=size)
            new_planet_texture.wrapped = False
            new_planet_texture.smoothed = True

            new_planet_texture.set_data(format, pitch, tex_data)

            TextureManager.get_instance().add_texture(new_planet_texture)
            
            #test_plane.node.renderer.material.texture = "planet_texture"
            
            #e = datetime.now() - b

            #print "%s Tex Gen Vid card copy time: %3.5f" % (address, e.total_seconds())#(e.seconds +  (e.microseconds / 1000000.0) ) )

            #new_planet_texture.image.save(texture_name+'.png')

            self._generated_textures[address] = texture_name

        return texture_name

    def get_texture(self, address, resolution=None):
        return self._gen_texture(address, resolution)
    
        
        