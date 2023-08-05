"""
Unit tests
Employing the unittest standard python test framework
https://docs.python.org/3/library/unittest.html
    
pyGLV (Computer Graphics for Deep Learning and Scientific Visualization)
@Copyright 2021-2022 Dr. George Papagiannakis

"""

import unittest

import pyECSS.utilities as util
from pyECSS.Entity import Entity
from pyECSS.Component import BasicTransform, Camera, RenderMesh
from pyECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyGLV.GL.Scene import Scene
from pyECSS.ECSSManager import ECSSManager

from pyGLV.GL.Shader import Shader

@unittest.skip("Requires active GL context, skipping the test")
class TestShader(unittest.TestCase):
    
    def setUp(self):
        print("TestShader:setUp START".center(100, '-'))
        
        self.myShader = Shader()
        
        
        print("TestShader:setUp END".center(100, '-'))
        
    
    def test_init(self):
        print("TestShader:test_init START".center(100, '-'))
        
        self.assertEqual(self.myShader.name, "Shader")
        self.assertEqual(self.myShader.type,"Shader")
        
        print("TestShader:test_init END".center(100, '-'))
    
    
    def test_update(self):
        print("TestShader:test_update START".center(100, '-'))
        
        
        
        print("TestShader:test_update END".center(100, '-'))
        

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=3, exit=False)