from camera import *
from screen import *

if __name__ == '__main__':
  c = Camera()
  s = Screen('3D Renderer', camera=c)
  
  # cube = Cube(center=Point(.5, .5, .5), radius=.5)
  sphere = Sphere(center=Point(.0, .0, .0), radius=1.0, segments=18)

  random_stars = [RandomPoint([-100.0, 100.0]) for _ in range(500)]

  # c.add_object(cube)
  c.add_object(sphere)
  c.add_objects(random_stars)

  c.set_axis_visible(True)

  s.play()
