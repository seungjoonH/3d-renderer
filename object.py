import numpy as np
from color import Color
import math

class Object:
  def get_coords(self): pass
  def get_render_data(self): pass

class Point(Object):
  def __init__(self, *args):
    self.color = Color.WHITE

    if len(args) == 1:
      self.x, self.y, self.z = args[0]

    elif len(args) == 2:
      vec, color = args
      self.x, self.y, self.z = vec

    elif len(args) == 3:
      self.x, self.y, self.z = args

    elif len(args) == 4:
      self.x, self.y, self.z, color = args

  def get_coords(self): 
    return np.array([self.x, self.y, self.z])

  def get_render_data(self):
    return 0, self.color

class Line(Object):
  def __init__(self, start, end, color=Color.WHITE):
    self.start = start
    self.end = end
    self.color = color

  def get_coords(self):
    return [self.start, self.end]

  def get_render_data(self):
    return 1, self.color

class Polygon(Object):
  def __init__(self, points, color=Color.WHITE):
    self.points = points
    self.color = color

  def get_coords(self):
    return self.points
  
  def get_render_data(self):
    return 2, self.color


class Axis(Line):
  def __init__(self, length=2, color=Color.WHITE):
    self.length = length
    self.start = np.array([0, 0, 0])
    self.end = None
    self.color = color

  def get_coords(self):
    return [self.start, self.end]
  
  def get_render_data(self):
    return 1, self.color

class XAxis(Axis):
  def __init__(self):
    super().__init__()
    self.end = np.array([self.length, 0, 0])
    self.color = Color.RED

class YAxis(Axis):
  def __init__(self):
    super().__init__()
    self.end = np.array([0, self.length, 0])
    self.color = Color.GREEN

class ZAxis(Axis):
  def __init__(self):
    super().__init__()
    self.end = np.array([0, 0, self.length])
    self.color = Color.BLUE

class Cube:
  def __init__(self, center, radius):
    self.center = center.get_coords()

    self.points = [
      Point(self.center - np.array([  radius,  radius,  radius])),
      Point(self.center - np.array([ -radius,  radius,  radius])),
      Point(self.center + np.array([  radius, -radius,  radius])),
      Point(self.center - np.array([  radius,  radius, -radius])),

      Point(self.center + np.array([  radius,  radius,  radius])),
      Point(self.center + np.array([ -radius,  radius,  radius])),
      Point(self.center - np.array([  radius, -radius,  radius])),
      Point(self.center + np.array([  radius,  radius, -radius]))
    ]

    self.polygons = [
      Polygon([self.points[0], self.points[1], self.points[2], self.points[3]]),
      Polygon([self.points[0], self.points[1], self.points[7], self.points[6]]),
      Polygon([self.points[0], self.points[3], self.points[5], self.points[6]]),
      Polygon([self.points[4], self.points[2], self.points[1], self.points[7]]),
      Polygon([self.points[4], self.points[7], self.points[6], self.points[5]]),
      Polygon([self.points[4], self.points[2], self.points[3], self.points[5]])
    ]

  def get_coords(self):
    return self.polygons
  
  def get_render_data(self):
    return 3, Color.WHITE
  

class Sphere:
  circle_segments = 50
  
  def __init__(self, center, radius, segments=20):
    self.center = center.get_coords()
    self.radius = radius
    self.segments = segments

    self.latitudes = [
      self.get_latitude(i - self.segments / 2)
      for i in range(self.segments)
    ]

    self.longitudes = [
      self.get_longitude(i)
      for i in range(self.segments)
      
    ]
    
    self.polygons = self.latitudes + self.longitudes

  def get_coords(self):
    return self.polygons
  
  def get_latitude(self, n):
    theta = math.pi / self.segments
    h = self.radius * math.sin(theta * n)
    r = self.radius * math.cos(theta * n)
    c = self.center + np.array([.0, h, .0])

    print(n, math.degrees(theta * n), r)

    dt = 2 * math.pi / Sphere.circle_segments
    points = [
      Point(c + r * np.array([math.cos(dt * i), 0, math.sin(dt * i)]))
      for i in range(Sphere.circle_segments)
    ]

    return Polygon(points)

  def get_longitude(self, n):
    theta = 2 * math.pi / Sphere.circle_segments
    dt = 2 * math.pi / self.segments

    points = [
      Point(self.center + self.radius * np.array([
        math.cos(theta * i) * math.cos(dt * n),
        math.sin(theta * i),
        math.cos(theta * i) * math.sin(dt * n)
      ]))
      for i in range(Sphere.circle_segments)
    ]

    return Polygon(points)

  def get_render_data(self):
    return 3, Color.WHITE
  