"""
무작위 점(RandomPoint) 데모.
실행: python main_randompoint.py
"""

import sys
import os
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'src'))

from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer — RandomPoint', camera=c)

  stars = [RandomPoint([-100.0, 100.0]) for _ in range(500)]
  c.add_objects(stars)
  c.set_axis_visible(True)
  s.play()
