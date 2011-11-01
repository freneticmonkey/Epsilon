
import sys, traceback

import pygame
from OpenGL.GL import *

class TestBase(object):
    
    def __init__(self, name=None):
        if name == None:
            name = "Unnamed Test"
        
        self._test_name = name
        self._quitting = False
        
        try:
            pygame.init()
            
            self.InitDisplay()
            
            self.Init()
            
            self.Run()
            
            self.Shutdown()
            
            self.Quit()
            
        except pygame.error, msg:
            print "PYGAME ERROR in test: " + self._test_name
            print "Error Message: " + msg
            print "Stack:"
            traceback.print_exc(file=sys.stdout)
            
        except:
            print "General ERROR in test: " + self._test_name
            print "Stack:"
            traceback.print_exc(file=sys.stdout)
            
        finally:
            self.Quit()
    
    # This is for Test Specific Initilisation
    def Init(self):
        pass
        
    def Quit(self):
        pygame.quit()
        
    def Run(self):
        
        if self._quitting:
            print "Test Ended. Do not call this function directly"
            return
        
        while not self._quitting:
            eventlist = pygame.event.get()
            
            # Check for quit
            for event in eventlist:
                if event.type == pygame.QUIT \
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self._quitting = True
            
            # Clear Buffer
            self.Clear()
            
            # Draw Scene      
            self.Draw()
            
            # Flip Buffers
            self.Flip()
        
        
    # This is overwritten by Tests that need to shutdown
    def Shutdown(self):
        pass  
        
    def InitDisplay(self):
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
        pygame.display.set_caption(self._test_name)
            
    def Clear(self):    
        # Clear to Blue
        glClearColor(180/255, 218/255, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    # This is overwritten by each of the tests
    def Draw(self):
        pass
        
    def Flip(self):
        pygame.display.flip()

if __name__ == "__main__":
    tb = TestBase()
    
    
            
        
