"""
정육면체(Cube) 데모.
실행: python main_cube.py
"""

import sys
import os
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'src'))

from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer — Cube', camera=c)

  c.add_object(Cube(center=Point(0.5, 0.5, 0.5), radius=0.5))
  c.set_axis_visible(True)
  s.play()
