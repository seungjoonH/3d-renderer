"""
다각형(Polygon) 데모.
실행: python main_polygon.py
"""

import sys
import os
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'src'))

from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer — Polygon', camera=c)

  # 삼각형
  tri = Polygon([
    Point(0.0, 0.0, 0.0),
    Point(1.0, 0.0, 0.0),
    Point(0.0, 1.0, 0.0),
  ])
  # 사각형
  quad = Polygon([
    Point(0.0, 0.0, 1.0),
    Point(1.0, 0.0, 1.0),
    Point(1.0, 1.0, 1.0),
    Point(0.0, 1.0, 1.0),
  ], color=Color.GREEN)

  c.add_object(tri)
  c.add_object(quad)
  c.set_axis_visible(True)
  s.play()
