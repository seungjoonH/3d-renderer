"""
구(Sphere) 데모.
실행: python main_sphere.py
"""

import sys
import os
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'src'))

from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer — Sphere', camera=c)

  c.add_object(Sphere(center=Point(0.0, 0.0, 0.0), radius=1.0, segments=18))
  c.set_axis_visible(True)
  s.play()
