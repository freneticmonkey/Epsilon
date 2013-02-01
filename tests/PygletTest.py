'''
Created on Mar 23, 2012

@author: scottporter
'''

import pyglet

from pyglet.window import key, mouse
from pyglet.gl import *

from pyglet import image

from random import random
import struct

import numpy

window = None
label = None

#def main():
window = pyglet.window.Window(800, 600, "Hello World", True, vsync=False)
label = pyglet.text.Label("Hello World label. This is another line of text", 
                          font_name="Arial",
                          font_size=24,
                          color = (0,0,255,255),
                          x=window.width/2,
                          y=window.height/2,
                          anchor_x="center",
                          anchor_y="center")
#image = pyglet.resource.image('screenshot.png')
#im = pyglet.resource.image('test_image.jpg')
#music = pyglet.resource.media("justice.mp3")
fps_display = pyglet.clock.ClockDisplay()

keys = key.KeyStateHandler()
window.push_handlers(keys)

#print int(image.get_image_data().get_data("RGBA",1024)[0])
#print image.get_image_data().get_data("RGBA",1024)


size = 128
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

im = image.create(size, size, image.CheckerImagePattern())

data = numpy.random.random_integers(low=0,
                                    high=1,
                                    size = (size * size, format_size))

data *= 255
#data[:,1:-1] = 0
data[:,3] = 255
data.shape = -1
tex_data = (GLubyte * data.size)(*data.astype('u1'))
pitch =  size * format_size

# dim = image.ImageData(size,size, "RGBA", tex_data, pitch )
im.set_data("RGBA", pitch, tex_data)

def update(dt):
    pass

@window.event
def on_draw():
    window.clear()
    im.blit(0,0)
    #label.draw()
    
    # glClear(GL_COLOR_BUFFER_BIT)
    # glLoadIdentity()
    # glBegin(GL_TRIANGLES)
    # glVertex2f(0,0)
    # glVertex2f(window.width, 0)
    # glVertex2f(window.width, window.height)
    # glEnd()
    
    fps_display.draw()
#    label._set_text("FPS: %3.2f" % pyglet.clock.get_fps())
#    label.draw()

@window.event
def on_key_press(symbol, modifiers):
    print "A key was pressed."
    #music.play()
    
    print str(keys)
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    print "Mouse button: %d pressed @ x: %d y: %d" % (button, x, y)

if __name__ == "__main__":
    #main()
    pyglet.clock.schedule(update)
    pyglet.app.run()
    
