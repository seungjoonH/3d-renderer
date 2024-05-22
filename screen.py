import pygame as pg
from color import Color
from key import Key
from object import *
import random

class Screen:
  size = [1200, 800]

  def __init__(self, title, camera, FPS=240):
    self.__clock = pg.time.Clock()
    self.__display = pg.display.set_mode(Screen.size)
    pg.display.set_caption(title)
    self.__display.fill(Color.BLACK)
    self.__camera = camera
    self.__FPS = FPS
    self.__key = Key()

  def render(self):
    data = self.__camera.get_render_data()

    for datum in data:
      dimension, color, coords = datum

      if dimension == 0:
        if coords is None: continue
        pg.draw.circle(self.__display, color, coords, 1)

      elif dimension == 1:
        if any(c is None for c in coords): continue
        pg.draw.line(self.__display, color, coords[0], coords[1])
      
      elif dimension == 2:
        pg.draw.lines(self.__display, color, True, coords)

      elif dimension == 3:
        for points in coords:
          points = [i for i in points if i is not None]
          if len(points) < 2: continue
          pg.draw.lines(self.__display, color, True, points)
  
  def play(self):
    running = True

    while running:
      # 배경색 설정
      self.__display.fill(Color.BLACK)

      for event in pg.event.get():
        # 창 닫기 버튼 클릭 시 종료
        if event.type == pg.QUIT:
          running = False
        
        # 마우스 입력 감지 시
        elif event.type == pg.MOUSEBUTTONDOWN:
          # WHEELUP - 확대
          if event.button == pg.BUTTON_WHEELUP: self.__camera.zoom_in()
          # WHEELDOWN - 축소
          elif event.button == pg.BUTTON_WHEELDOWN: self.__camera.zoom_out()

        # 키보드 입력 감지 시
        elif event.type == pg.KEYDOWN:
          self.__key.set_press(event.key)

          # ESC - 종료
          if self.__key.is_pressed('ESC'): running = False
          # Q - 종료
          if self.__key.is_pressed('Q'): running = False
          # F - 뒤 돌기
          if self.__key.is_pressed('F'): self.__camera.turn_back()

      held = pg.key.get_pressed()
      self.__key.set_hold(held)

      # W - 앞으로 이동
      if self.__key.is_held('W'): self.__camera.move('F')
      # S - 뒤로 이동
      if self.__key.is_held('S'): self.__camera.move('B')
      # A - 좌측 이동 
      if self.__key.is_held('A'): self.__camera.move('L')
      # D - 우측 이동 
      if self.__key.is_held('D'): self.__camera.move('R')
      # SPACE - 위로 이동
      if self.__key.is_held('SPACE'): self.__camera.move('U')
      # SHIFT - 아래로 이동
      if self.__key.is_held('SHIFT'): self.__camera.move('D')

      # CTRL - 이동 시 5배 가속
      velocity = 5 if self.__key.is_held('CTRL') else 1
      self.__camera.set_moving_velocity(velocity)

      # 마우스 커서 화면 중앙 고정
      pg.mouse.set_pos(Screen.size[0] * .5, Screen.size[1] * .5)
      # 마우스 커서 숨김
      pg.mouse.set_visible(False)

      Screen.delta_pos = pg.mouse.get_rel()

      if sum(bool(pos) for pos in Screen.delta_pos) > 0:
        self.__camera.rotate()



      self.render()

      self.__clock.tick(self.__FPS)
      pg.display.flip()

    pg.quit()