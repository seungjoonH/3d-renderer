import pygame as pg

class Key:
  __data = {
    'W': [pg.K_w, 12616],
    'A': [pg.K_a, 12609],
    'S': [pg.K_s, 12596],
    'D': [pg.K_d, 12615],
    'Q': [pg.K_q, 12610],
    'F': [pg.K_f, 12601],
    'ESC': [pg.K_ESCAPE],
    'SPACE': [pg.K_SPACE],
    'CTRL': [pg.K_LCTRL],
    'SHIFT': [pg.K_LSHIFT],
  }

  def set_press(self, pressed):
    self.pressed = pressed

  def set_hold(self, held):
    self.held = held

  def is_pressed(self, key):
    return self.pressed in Key.__data[key]
    
  def is_held(self, key):
    any_in = lambda group: any([self.held[k] for k in group])
    return any_in(Key.__data[key])
    