'''
Created on Mar 23, 2012

@author: scottporter
'''

import pyglet

from pyglet.window import key, mouse
from pyglet.gl import *

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
image = pyglet.resource.image('screenshot.png')
#music = pyglet.resource.media("justice.mp3")
fps_display = pyglet.clock.ClockDisplay()

keys = key.KeyStateHandler()
window.push_handlers(keys)

def update(dt):
    pass

@window.event
def on_draw():
    window.clear()
    #image.blit(0,0)
    #label.draw()
    
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glVertex2f(0,0)
    glVertex2f(window.width, 0)
    glVertex2f(window.width, window.height)
    glEnd()
    
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
    
