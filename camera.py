import numpy as np
from object import *
from screen import Screen
import math

class Camera:
  # 원점
  o = np.array([ .0,  .0,  .0])

  # 3차원 공간단위벡터
  i = np.array([1.0,  .0,  .0])
  j = np.array([ .0, 1.0,  .0])
  k = np.array([ .0,  .0, 1.0])

  # 화면 크기
  w, h = Screen.size
  
  # 좌표-픽셀간 비율
  ratio = 1000

  # 속력
  init_moving_velocity = .01
  init_rotate_velocity = .03

  def __init__(self):
    # 시점
    self.v = np.array([3.0, 3.0, 3.0])
    self.v_norm = np.linalg.norm(self.v)

    # 시선벡터
    self.p_norm = .5
    self.p = -self.v / self.v_norm * self.p_norm
    
    # 화면의 단위법선벡터
    self.n = self.p / self.p_norm

    # 화면의 정중앙점
    self.c = self.v + self.p
    
    # 속력
    self.moving_velocity = Camera.init_moving_velocity
    self.rotate_velocity = Camera.init_rotate_velocity

    self.axis_visible = True

    self.__objects = []

    self.update()

  # 화면 최신화
  def update(self):
    self.v_norm = np.linalg.norm(self.v)
    self.p_norm = np.linalg.norm(self.p)

    self.c = self.v + self.p
    self.n = self.p / self.p_norm

    px, py, pz = self.p
    px_sign, py_sign, pz_sign = map(np.sign, self.p)
    px_abs, py_abs, pz_abs = map(np.abs, self.p)
    
    ix = iy = iz = .0
    jx = jy = jz = .0

    px_py = math.sqrt(px ** 2 + py ** 2) 
    py_pz = math.sqrt(py ** 2 + pz ** 2) 
    pz_px = math.sqrt(pz ** 2 + px ** 2) 
    
    if px and py:
      # px != 0, py != 0
      ix = pz / pz_px
      iz = -px / pz_px

      alpha = - (px ** 2 + pz ** 2) / (px * py)
      beta = pz / px

      j_norm = math.sqrt(1 + alpha ** 2 + beta ** 2)
      jx, jy, jz = np.array([1, alpha, beta]) / j_norm

    elif px and not py:
      # px != 0, py == 0, pz != 0
      if pz: 
        ix = px_sign * pz_abs / pz_px
        iz = -pz_sign * px_abs / pz_px
        jx, jy, jz = 0, -1, 0

      # px != 0, py == 0, pz == 0
      else:
        iz = -px_sign
        jy = px_sign
    
    elif not px and py:
      # px == 0, py != 0, pz != 0
      if pz:
        ix = py_sign
        jy = -pz_abs / py_pz
        jz = pz_sign * py / py_pz

      # px == 0, py != 0, pz == 0
      else:
        ix = -py_sign / math.sqrt(2)
        iz =  py_sign / math.sqrt(2)
        jx = -py_sign / math.sqrt(2)
        jz = -py_sign / math.sqrt(2)

    else:
      ix = pz_sign
      jy = pz_sign

    self.i_prime = np.array([ix, iy, iz])
    self.j_prime = np.array([jx, jy, jz])

    if self.j_prime[1] > 0: self.j_prime *= -1

    self.__axis = [XAxis(), YAxis(), ZAxis()]

  # 객체 집합 비우기
  def clear_objects(self):
    self.__objects.clear()

  # 한 객체 추가
  def add_object(self, obj):
    self.__objects.append(obj)
  
  # 여러 객체 추가
  def add_objects(self, objs):
    self.__objects += objs

  # 객체 집합 교체
  def set_objects(self, *objs):
    self.__objects = objs[:]

  # 객체 집합의 원소를 각각 좌표 변환
  def convert_coords(self, vecs):
    arr = []

    if isinstance(vecs, np.ndarray):
      return self.convert_coord(vecs)
    elif isinstance(vecs, Point):
      return self.convert_coord(vecs.get_coords())
    elif isinstance(vecs, Polygon):
      arr = vecs.get_coords()[:]
    elif isinstance(vecs, list):
      arr = vecs[:]

    return [self.convert_coords(x) for x in arr]

  # 좌표 변환 (3차원 -> 2차원)
  def __convert_coord(self, a):
    cx, cy, cz = self.c
    px, py, pz = self.p
    ax, ay, az = a

    av = a - self.v
    avx, avy, avz = av

    denominator = px * (cx - ax) + py * (cy - ay) + pz * (cz - az)
    numerator = px * avx + py * avy + pz * avz

    if not numerator: return None
    t = denominator / numerator

    x, y, z = ax + avx * t, ay + avy * t, az + avz * t
    A_prime = np.array([x, y, z])

    A_prime_v = A_prime - self.v

    div = np.array([.0, .0, .0])

    for i in range(3):
      if av[i]: div[i] = A_prime_v[i] / av[i]
      else: div[i] = .0

    if not (0 < sum(div) <= 3):
      return None
    
    a_prime = A_prime - self.c

    a_prime_x_norm = np.dot(a_prime, self.i_prime) * Camera.ratio
    a_prime_y_norm = np.dot(a_prime, self.j_prime) * Camera.ratio

    a_prime_screen = np.array([a_prime_x_norm, a_prime_y_norm])

    return a_prime_screen
  
  # 좌표 변환 (3차원 -> 2차원)
  def convert_coord(self, a):
    a_prime_screen = self.__convert_coord(a)

    if a_prime_screen is None: return None

    x, y = a_prime_screen
    x += Camera.w / 2
    y += Camera.h / 2

    return np.array([x, y])

  def get_render_data(self):
    data = []
    objects = []
    if self.axis_visible: objects = self.__axis[:]
    objects += self.__objects[:]

    for obj in objects:
      func, color = obj.get_render_data()
      coords = self.convert_coords(obj.get_coords())
      data.append([func, color, coords])
    return data

  # 확대
  def zoom_in(self):
    self.p_norm = min(self.p_norm + .01, 3)
    self.p = self.n * self.p_norm
    self.update()

  # 축소
  def zoom_out(self):
    self.p_norm = max(self.p_norm - .01, .1)
    self.p = self.n * self.p_norm
    self.update()

  def __rotate(self, delta):
    delta_x, delta_y = np.array(delta)
    delta_x /= Camera.w / (self.rotate_velocity * 50)
    delta_y /= Camera.h / (self.rotate_velocity * 50)
    
    dx = delta_x * self.i_prime
    dy = delta_y * self.j_prime

    ndx = self.n + dx
    ndy = self.n + dy
    n = ndx + ndy
    
    self.n = n / np.linalg.norm(n)
    self.p = self.n * self.p_norm
    
    self.update()

  # 시선전환
  def rotate(self):
    self.__rotate(Screen.delta_pos)

  def __move(self, delta):
    self.v += delta
    self.update()

  # 시점 위치이동
  def move(self, direction):
    self.camera_moving = CameraMoving(direction, self.moving_velocity)
    lr = self.i_prime
    ud = -Camera.j
    fb = self.n
    self.camera_moving.sync(self.v, lr, ud, fb)
    delta = self.camera_moving.get_delta()
    self.__move(delta)

  def set_moving_velocity(self, scale):
    self.moving_velocity = Camera.init_moving_velocity * scale

  # 뒤 돌기
  def turn_back(self):
    self.p = -self.p
    self.update()
    
  # 공간 축 표시
  def set_axis_visible(self, visible):
    self.axis_visible = visible

class CameraMoving:
  def __init__(self, direction, velocity):
    self.direction = direction
    self.velocity = velocity

  def sync(self, v, lr, ud, fb):
    self.v = v
    self.lr = lr
    self.ud = ud
    self.fb = fb

  def get_delta(self):
    if self.direction  == 'L':
      return -self.lr * self.velocity
    elif self.direction  == 'R':
      return self.lr * self.velocity
    elif self.direction  == 'U':
      return -self.ud * self.velocity
    elif self.direction  == 'D':
      return self.ud * self.velocity
    elif self.direction  == 'F':
      return self.fb * self.velocity
    elif self.direction  == 'B':
      return -self.fb * self.velocity