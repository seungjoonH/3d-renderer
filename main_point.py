"""
점(Point) 데모.
실행: python main_point.py
"""

import sys
import os
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'src'))

from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer — Point', camera=c)

  c.add_object(Point(0.0, 0.0, 0.0))
  c.add_object(Point(1.0, 0.0, 0.0, Color.RED))
  c.add_object(Point(0.0, 1.0, 0.0, Color.GREEN))
  c.add_object(Point(0.0, 0.0, 1.0, Color.BLUE))
  c.set_axis_visible(True)
  s.play()
