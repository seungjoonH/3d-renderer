"""
폴리곤 메쉬(점 + 삼각형 인덱스) 데모.
실행: python main_mesh.py
"""

import sys
import os
_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_root, 'src'))

from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer — Polygon Mesh', camera=c)

  point_data = [
    (6, -6, -32), (-6, -6, -32), (-6, 6, -32), (-6, -6, 31.9999981),
    (6, -3.37361646, -32), (3.03399444, 3.03399444, -32), (1.66106641, 6, -32),
    (-3.55527568, -3.5552752, 31.9999981), (-6, 1.72618556, 31.9999981),
    (-2.42364287, -5.99999905, 32), (5.99999905, -5.99999905, -23.9282894),
    (-6, 4.43757248, 23.6670475), (-6, 6, 18.8652096), (-1.75159454, 6, -9.34183311),
  ]
  triangle_indices = [
    (0, 1, 4), (1, 5, 4), (1, 2, 5), (2, 6, 5), (3, 7, 8), (3, 9, 7),
    (0, 4, 10), (3, 0, 9), (0, 10, 9), (0, 3, 1), (1, 3, 11), (3, 8, 11),
    (2, 1, 12), (1, 11, 12), (2, 13, 6), (2, 12, 13), (10, 4, 5), (10, 5, 6),
    (10, 6, 13), (10, 13, 12), (10, 12, 11), (10, 11, 8), (10, 8, 7), (10, 7, 9),
  ]

  points = [Point(x, y, z) for x, y, z in point_data]
  polygons = [Polygon([points[i], points[j], points[k]]) for i, j, k in triangle_indices]
  c.add_objects(polygons)
  c.set_axis_visible(True)
  s.play()
