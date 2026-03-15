"""
선(Line) 데모.
실행: python main_line.py
"""

import sys
import os
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'src'))

from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer — Line', camera=c)

  c.add_object(Line(Point(0.0, 0.0, 0.0), Point(1.0, 2.0, 3.0)))
  c.add_object(Line(Point(-1.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Color.RED))
  c.set_axis_visible(True)
  s.play()
