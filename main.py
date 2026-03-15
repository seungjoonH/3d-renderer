"""
3D Renderer 진입점.
실행: python main.py  또는  python3 main.py
CLI에서 방향키로 도형을 고르고 Enter 로 실행합니다.
"""

import sys
import os
import subprocess

DEMOS = [
  ('Point', 'main_point.py'),
  ('RandomPoint', 'main_randompoint.py'),
  ('Line', 'main_line.py'),
  ('Polygon', 'main_polygon.py'),
  ('Cube', 'main_cube.py'),
  ('Sphere', 'main_sphere.py'),
  ('Polygon Mesh', 'main_mesh.py'),
]


def getkey_unix():
  import tty
  import termios
  fd = sys.stdin.fileno()
  old = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    c = sys.stdin.read(1)
    if c == '\x1b':
      c2 = sys.stdin.read(1)
      if c2 == '[':
        c3 = sys.stdin.read(1)
        if c3 == 'A': return 'up'
        if c3 == 'B': return 'down'
    if c in '\r\n': return 'enter'
    return c
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)


def getkey_win():
  import msvcrt
  c = msvcrt.getch()
  if c in (b'\r', b'\n'): return 'enter'
  if c == b'\xe0': 
    c2 = msvcrt.getch()
    if c2 == b'H': return 'up'
    if c2 == b'P': return 'down'
  try: return c.decode('utf-8')
  except Exception: return None


def getkey():
  if sys.platform == 'win32': return getkey_win()
  return getkey_unix()


def run_menu():
  index = 0
  n = len(DEMOS)

  while True:
    os.system('cls' if sys.platform == 'win32' else 'clear')
    print('  어떤 도형 데모를 실행할까요? \n')
    for i, (label, _) in enumerate(DEMOS):
      prefix = '  > ' if i == index else '    '
      print(f'{prefix} {label}')
    print()

    key = getkey()
    if key == 'up': index = (index - 1) % n
    elif key == 'down': index = (index + 1) % n
    elif key == 'enter': return index
    else:
      try:
        num = int(key)
        if 1 <= num <= n: return num - 1
      except ValueError: pass


def main():
  base = os.path.dirname(os.path.abspath(__file__))
  sys.path.insert(0, base)

  try:
    idx = run_menu()
  except (ImportError, OSError, AttributeError):
    print('  어떤 도형 데모를 실행할까요?\n')
    for i, (label, _) in enumerate(DEMOS, 1):
      print(f'    {i}. {label}')
    print()
    while True:
      try:
        choice = input(f'  번호 입력 (1–{len(DEMOS)}): ').strip()
        idx = int(choice) - 1
        if 0 <= idx < len(DEMOS): break
      except ValueError: pass
    print()

  _, script = DEMOS[idx]
  script_path = os.path.join(base, script)
  if not os.path.isfile(script_path):
    print(f'  오류: {script} 을(를) 찾을 수 없습니다.')
    sys.exit(1)
  subprocess.run([sys.executable, script_path], cwd=base)


if __name__ == '__main__':
  main()
