'''
Created on Apr 8, 2012

@author: scottporter
'''

from Render.ShaderTree.ShaderTree import ShaderTree
from Render.ShaderTree.ShaderNodes import MaterialNode, ViewerOutputNode

def main():
    
    print "Building Shader"
    tree = ShaderTree("BasicShader")
    material = MaterialNode(tree)
    viewer = ViewerOutputNode(tree)
    
    # Vertex Shader
    # NYI
    
    # Fragment Shader
    tree.add_data(material)
    tree.add_node(viewer)
    
    # Add connection - maybe this needs to be reversed to be more readable
    # destination connects to the source
    viewer.connect("output", material, "diffuse")
    
    print "Generating Source"
    
    # Generate Source
    tree.process_tree()
    
    print ""
    print "Source Generated"
    print "================"
    print tree.source


if __name__ == "__main__":
    main()
