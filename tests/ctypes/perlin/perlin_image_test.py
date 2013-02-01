'''
Created on Mar 23, 2012

@author: scottporter
'''

from datetime import datetime

import pyglet

from pyglet.window import key, mouse
from pyglet.gl import *

from pyglet import image

from random import random
import struct

import numpy

from cperlin import Perlin, FractalNoise

#from noise import pnoise3, snoise3
from noise import _simplex, _perlin

import math

from Queue import Queue
import threading

# from multiprocessing import Queue as pQueue
# from multiprocessing import Process
import multiprocessing
from multiproc_example import Consumer, NoiseTask, ProcessingRange

from threaded_noise import NoiseThread#, NoiseProcess

# window = None
# label = None

class PygletTest(object):
  def __init__(self):
    self.setup()

  def setup(self):
    self._window = pyglet.window.Window(1900, 1040, "Hello World", True, vsync=False)
    label = pyglet.text.Label("Hello World label. This is another line of text", 
                              font_name="Arial",
                              font_size=24,
                              color = (0,0,255,255),
                              x=self._window.width/2,
                              y=self._window.height/2,
                              anchor_x="center",
                              anchor_y="center")

    self._window.on_draw = self.on_draw
    #self._window.on_key_press = self.on_key_press
    self._window.on_mouse_press = self.on_mouse_press

    #image = pyglet.resource.image('screenshot.png')
    #im = pyglet.resource.image('test_image.jpg')
    #music = pyglet.resource.media("justice.mp3")
    self._fps_display = pyglet.clock.ClockDisplay()

    self._keys = key.KeyStateHandler()
    self._window.push_handlers(self._keys)

    self._image_size = 512

  def single_threaded_image(self):
    
    # perlin = Perlin(12345)
    # frac = FractalNoise(h=1.0, lacunarity=50.0, octaves=4.2, noise=perlin )

    perlin_data = []

    x = 0#self._image_size

    octaves = 6.0
    ioct = int(octaves)

    scale = 2 * octaves

    ls3 = 10 * octaves

    ls2 = 15 * octaves

    ls = 20 * octaves

    for y in xrange(self._image_size):
      for z in xrange(self._image_size):
        #value = ( (perlin.noise3(float(x) / scale, float(y) / scale, z) * 127.0) + 128.0)
        # value = pnoise3(float(x) / scale, float(y) / scale, z) * 127.0 + 128.0
        # value = snoise3(float(x) / scale, float(y) / scale, z) * 127.0 + 128.0
        # value = perlin.noise3(x,y,z)

        #value = frac.ridged_multi_fractal3(float(x) / scale, float(y) / scale, z, 0, 1.0)

        #value = snoise3(float(x) / scale, float(y) / scale, z)

        #value = _simplex.noise3(float(x) / scale, float(y) / scale, z, 32, 1.0)#, base=0)
      
        ######
        # value = _perlin.noise3(float(x) / ls, float(y) / ls, z / ls, octaves, 0.5)#, base=0)

        # if value > 0.8 or value < 0:
        #   value = -1
        # else:
        #   value += _perlin.noise3(float(x) / scale, float(y) / scale, z / ls, octaves, 0.5)#, base=0)
      
        #   value += _perlin.noise3(float(x) / ls2, float(y) / ls2, z / ls, octaves, 0.5)#, base=0)

        #   value += _perlin.noise3(float(x) / ls3, float(y) / ls3, z / ls, octaves, 0.5)#, base=0)
        ####

        value = _perlin.noise3(x / ls, y / ls, z / ls, ioct, 0.5)#, base=0)

        if value > 0.8 or value < 0:
          value = -1
        else:
          value += _perlin.noise3(x / scale, y / scale, z / scale, ioct, 0.5)#, base=0)
          value += _perlin.noise3(x / ls2, y / ls2, z / ls2, ioct, 0.5)#, base=0)
          value += _perlin.noise3(x / ls3, y / ls3, z / ls2, ioct, 0.5)#, base=0)


        # value *= 1000
        #print value
        #value = max(min(value, 0.6), 0.4)

        # value += math.cos(x + value)

        # value *= 20
        # value = value - int(value)

        #value += frac.ridged_multi_fractal3(float(x) / scale, float(y) / scale, z, 0, 1.0)

        value = value * 127.0 + 128.0
        perlin_data += [value, value, value, 1.0] 

    return perlin_data   

  def multi_threaded_image(self):
    num_threads = 16

    print "Number of threads: %d" % num_threads

    def producer(q, size, num):
      trange = size / num
      for i in range(0, num):
        thread = NoiseThread(size, i, i*trange, (i*trange)+trange)
        thread.start()
        q.put(thread, True)

    finished = []
    data = [None] * num_threads

    def consumer(q, num):
      while len(finished) < num:
        thread = q.get(True)
        thread.join()
        data[thread.get_position()] = thread.get_noise()
        finished.append(True)    

    q = Queue(num_threads)
    prod_thread = threading.Thread(target=producer, args=(q, self._size, num_threads))
    cons_thread = threading.Thread(target=consumer, args=(q, num_threads))
    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()

    #return [n for sublist in data for n in sublist]
    ret = []
    for a in data:
      ret += a
    return ret

  def multi_proc_image(self, face):
    
    # Establish communication queues
    tasks = multiprocessing.Queue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, results)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    # num_jobs = 10
    # for i in xrange(num_jobs):
    #     tasks.put(Task(i, i))

    size = 512
    num_jobs = 8

    # Hardcoded back face at the moment

    for i in range(0, num_jobs):
        tasks.put(NoiseTask(ProcessingRange(size, i, num_jobs, face)))
    
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)
    
    data = [None] * num_jobs

    # Start printing results
    while num_jobs:
        result = results.get()
        data[result[1]] = result[2]
        #print 'Result:', result
        num_jobs -= 1
    print "Finished"

    #return [n for sublist in data for n in sublist]
    ret = []
    for a in data:
      ret += a
    return ret


  def generate_image(self):

    #print int(image.get_image_data().get_data("RGBA",1024)[0])
    #print image.get_image_data().get_data("RGBA",1024)


    self._size = 512
    format_size = 4
    # data = []
    # for x in xrange(size * format_size):
    #   for y in xrange(size * format_size):
    #     if (x * y) + 1 % format_size == 0:
    #       data.append(255)  
    #     else:
    #       data.append(int(random() * 255))

    # d = struct.pack('B'*len(data), *data)
    # #tex_data = (GLubyte * 1)( *d )

    # imd = image.ImageData(size, size, 'RGBA', d)

    # im.blit_from(imd, 0, 0)

    start = datetime.now()

    self._back = image.create(self._image_size, self._image_size, image.CheckerImagePattern())

    # data = numpy.random.random_integers(low=0,
    #                                     high=1,
    #                                     size = (size * size, format_size))

    perlin_data = self.single_threaded_image()
    #perlin_data = self.multi_threaded_image()
    #perlin_data = self.multi_proc_image(0)


    el = datetime.now() - start

    print "Elapsed: %d.%3.0f" % ( el.seconds, el.microseconds / 1000.0)

    self._set_image_data(self._back, perlin_data)

    # data = numpy.array(perlin_data)

    # #data *= 255
    # #data[:,1:-1] = 0
    # # data[:,3] = 255
    # data.shape = -1
    # tex_data = (GLubyte * data.size)(*data.astype('u1'))
    # pitch =  self._size * format_size

    # # dim = image.ImageData(size,size, "RGBA", tex_data, pitch )
    # self._back.set_data("RGBA", pitch, tex_data)


  def _set_image_data(self, image, perlin_data):
    format_size = 4

    data = numpy.array(perlin_data)
    data.shape = -1
    tex_data = (GLubyte * data.size)(*data.astype('u1'))
    pitch =  self._image_size * format_size

    image.set_data("RGBA", pitch, tex_data)

  def gen_cube_map(self):
    
    self._right = image.create(self._image_size, self._image_size, image.CheckerImagePattern()) 
    self._back = image.create(self._image_size, self._image_size, image.CheckerImagePattern())
    self._left = image.create(self._image_size, self._image_size, image.CheckerImagePattern()) 
    # self._front = image.create(self._image_size, self._image_size, image.CheckerImagePattern())
    # self._top = image.create(self._image_size, self._image_size, image.CheckerImagePattern()) 
    # self._bottom = image.create(self._image_size, self._image_size, image.CheckerImagePattern())

    # # TOP
    # face = 0
    # start = datetime.now()
    # self._set_image_data(self._top, self.multi_proc_image(face))
    # el = datetime.now() - start
    # print "Face: %d Elapsed: %d.%3.0f" % (face, el.seconds, el.microseconds / 1000.0)
    
    # BACK
    face = 1
    start = datetime.now()
    self._set_image_data(self._back, self.multi_proc_image(face))
    el = datetime.now() - start
    print "Face: %d Elapsed: %d.%3.0f" % (face, el.seconds, el.microseconds / 1000.0)
    
    # RIGHT
    face = 2
    start = datetime.now()
    self._set_image_data(self._right, self.multi_proc_image(face))
    el = datetime.now() - start
    print "Face: %d Elapsed: %d.%3.0f" % (face, el.seconds, el.microseconds / 1000.0)
    
    # # BOTTOM
    # face = 3
    # start = datetime.now()
    # self._set_image_data(self._bottom, self.multi_proc_image(face))
    # el = datetime.now() - start
    # print "Face: %d Elapsed: %d.%3.0f" % (face, el.seconds, el.microseconds / 1000.0)
    
    # # FRONT
    # face = 4
    # start = datetime.now()
    # self._set_image_data(self._front, self.multi_proc_image(face))
    # el = datetime.now() - start
    # print "Face: %d Elapsed: %d.%3.0f" % (face, el.seconds, el.microseconds / 1000.0)
    
    # LEFT
    face = 5
    start = datetime.now()
    self._set_image_data(self._left, self.multi_proc_image(face))
    el = datetime.now() - start
    print "Face: %d Elapsed: %d.%3.0f" % (face, el.seconds, el.microseconds / 1000.0)
    
    

  def run(self):
    pyglet.clock.schedule(self.update)
    pyglet.app.run()

  def update(self, dt):
      pass

  #@window.event
  def on_draw(self):
      self._window.clear()

      #self._right.blit( 0,                  self._image_size)
      self._back.blit(  self._image_size,   self._image_size)
      #self._left.blit(  self._image_size*2, self._image_size)
      # self._front.blit( self._image_size*3, self._image_size)
      # self._bottom.blit(self._image_size,   0)
      # self._top.blit(   self._image_size,   self._image_size*2)
      #label.draw()
      
      # glClear(GL_COLOR_BUFFER_BIT)
      # glLoadIdentity()
      # glBegin(GL_TRIANGLES)
      # glVertex2f(0,0)
      # glVertex2f(window.width, 0)
      # glVertex2f(window.width, window.height)
      # glEnd()
      
      self._fps_display.draw()
  #    label._set_text("FPS: %3.2f" % pyglet.clock.get_fps())
  #    label.draw()

  #@window.event
  def on_key_press(self, symbol, modifiers):
      print "A key was pressed."
      #music.play()
      
      #print str(self._keys)
      
  #@window.event
  def on_mouse_press(self, x, y, button, modifiers):
      print "Mouse button: %d pressed @ x: %d y: %d" % (button, x, y)

if __name__ == "__main__":
    pg = PygletTest()
    pg.generate_image()
    #pg.gen_cube_map()
    pg.run()
    
