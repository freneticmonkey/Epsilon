'''
Created on Sep 22, 2011

@author: scottporter
'''

'''
Convert a list of lists into a flattened ctypes array, eg:
[ (1, 2, 3), (4, 5, 6) ] -> (GLfloat*6)(1, 2, 3, 4, 5, 6)
'''
def CreateGLArray(gltype, seq, length):
    arraytype = gltype * length
    return arraytype(*seq)