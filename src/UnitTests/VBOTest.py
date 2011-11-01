from OpenGL.GL import *
from OpenGL.GL.shaders import *

from OpenGL.arrays import vbo
import numpy
import Image

from TestBase import TestBase

class VBOTest(TestBase):
    
    def __init__(self):
        TestBase.__init__(self, name="VBO Test")
        
        
    def Init(self):
        try:
            vertex_shader = compileShader("""
            
            uniform float end_fog;
            uniform vec4 fog_color;
            
            void main()
            {
                float fog;
                float fog_coord; 
            
                //gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                gl_Position = ftransform();
                fog_coord = abs(gl_Position.z);
                fog_coord = clamp( fog_coord, 0.0, end_fog);
                fog = (end_fog - fog_coord)/end_fog;
                fog = clamp(fog, 0.0, 1.0);
                gl_FrontColor = mix(fog_color, gl_Color, fog);
            }
            """, GL_VERTEX_SHADER)
        except RuntimeError,err:
            print "Vertex Shader Compile Error: ", err
        
        try:
            frag_shader = compileShader("""
            //varying vec4 vertex_color;
            void main()
            {
                gl_FragColor = gl_Color;//vertex_color; //vec4(0,1,0,1);
            }
            """, GL_FRAGMENT_SHADER)
        except RuntimeError,err:
            print "Fragment Shader Compile Error: ", err
            
        self._shader = compileProgram(vertex_shader,frag_shader)
        
        self._shader_uniforms = {'end_fog'  : glGetUniformLocation(self._shader, 'end_fog'),
                                 'fog_color': glGetUniformLocation(self._shader, 'fog_color'),
                                }
        
        # Vertex 3 floats, Texture Coords 2 floats, Vertex Colour 3 floats
        
        self._vbo = vbo.VBO(
                            numpy.array([
                                            [  0, 1, 0, 0.5, 1.0, 0, 1, 0],
                                            [ -1,-1, 0, 0.0, 0.0, 1, 1, 0],
                                            [  1,-1, 0, 1.0, 0.0, 0, 1, 1]#,
#                                            [  2,-1, 0, 0.0, 0.0, 1, 0, 0],
#                                            [  4,-1, 0, 1.0, 0.0, 0, 1, 0],
#                                            [  4, 1, 0, 1.0, 1.0, 0, 0, 1],
#                                            [  2,-1, 0, 0.0, 0.0, 1, 0, 0],
#                                            [  4, 1, 0, 1.0, 1.0, 0, 0, 1],
#                                            [  2, 1, 0, 0.0, 1.0, 0, 1, 1],
                                        ],'f')
                            )
        print "VBO created"
        
        self.use_texture = False
        
        if self.use_texture:
            # Load Texture from disk
            image = Image.open("screenshot.png")
            image_x = image.size[0]
            image_y = image.size[1]
            try:
                image_data = image.tostring("raw","RGBA",0,-1)
            except SystemError:
                image_data = image.tostring("raw","RGBX",0,-1)
            
    #        image_data_2 = numpy.array(list(image.getdata()), numpy.int8)
            
            # Setup the GL Texture and its properties
            self._image_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self._image_id)
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            
            # Copy image data into the Texture buffer
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_x, image_y, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        
        
    def Draw(self):
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        
        glUseProgram(self._shader)
        
        try:
            self._vbo.bind()
            try:
                if self.use_texture:
                    # Setup the texture
                    glEnable(GL_TEXTURE_2D)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
                    glBindTexture(GL_TEXTURE_2D, self._image_id)
                
                # Move the triangle into a better position to display the fog effect
                glTranslate(0,0,0)
                glRotate(45,1,1,0)
                
                # Configure the Fog
                glUniform1f(self._shader_uniforms['end_fog'], 1)
                glUniform4f(self._shader_uniforms['fog_color'],1,1,1,1)
                
                # Enable States
                glEnableClientState(GL_TEXTURE_COORD_ARRAY)
                glEnableClientState(GL_VERTEX_ARRAY);
                glEnableClientState(GL_COLOR_ARRAY)
                
                # Configure VBO Pointers
                glVertexPointer(3, GL_FLOAT, 32, self._vbo)
                glTexCoordPointer(2, GL_FLOAT, 32, self._vbo+12)
                glColorPointer(3, GL_FLOAT,32, self._vbo+20)                
                
                glDrawArrays(GL_TRIANGLES,0,9)
            finally:
                self._vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY);
                glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        
        finally:
            glUseProgram(0)
        
        glPopMatrix()
        
    def Shutdown(self):
        print "Running VBO Shutdown"

if __name__ == "__main__":
    VBOTest()
    