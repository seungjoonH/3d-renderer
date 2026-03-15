# 3D Renderer

## 개요

3차원 공간의 도형을 2차원 화면에 투영하는 방식을 Python 으로 직접 구현해본 **3D 렌더링 실험 프로젝트** 입니다.

#### 기술 스택

<span>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white">
  <img src="https://img.shields.io/badge/Pygame-EE682A?style=for-the-badge&logo=pygame&logoColor=white">
</span>

<br />

## 실행 화면

### 움직이는 방법

마우스 회전 (시선 방향만 회전)

<img src="https://github.com/user-attachments/assets/fdca583a-8aae-49d3-ae3d-f77fef90ce9d" width="580" alt="screen-mouse-rotate" />
<br />
<br />

시점 이동 (WASD, Space, Shift)

<img src="https://github.com/user-attachments/assets/c9915e2c-eb14-493e-82fe-7ccaede3bd44" width="580" alt="screen-move" />
<br />
<br />

줌 (마우스 휠)

<img src="https://github.com/user-attachments/assets/8caa3988-8d99-4e2b-8f67-613e15fb78c6" width="580" alt="screen-zoom" />
<br />
<br />

<br />

### 도형 렌더링

점 (Point)

<img src="https://github.com/user-attachments/assets/eea36eba-9cac-4c0d-8c0d-246c583ea66d" width="580" alt="screen-point" />
<br />
<br />

무작위 점 (RandomPoint)

<img src="https://github.com/user-attachments/assets/e8261fc5-8086-4a13-a4c8-9b1dce1c77ba" width="580" alt="screen-randompoint" />
<br />
<br />

선 (Line)

<img src="https://github.com/user-attachments/assets/0de8ec01-421c-4e5d-8f36-4896a06d22cd" width="580" alt="screen-line" />
<br />
<br />

다각형 (Polygon)

<img src="https://github.com/user-attachments/assets/37575dd3-83d0-4854-90f6-d86e6a558da8" width="580" alt="screen-polygon" />
<br />
<br />

정육면체

<img src="https://github.com/user-attachments/assets/9e81bbcf-88a9-4950-a248-646fcc37fcb9" width="580" alt="screen-cube" />
<br />
<br />

구

<img src="https://github.com/user-attachments/assets/81856730-f95e-4af5-8c15-fd3bde63e8c1" width="580" alt="screen-sphere" />
<br />
<br />

<br />

## 사용법

### 키보드로 움직이기

<table>
<tr>
<td><img src="https://github.com/user-attachments/assets/110d9c63-a828-439a-9e29-3bdc6bbd2021" width="320" alt="diagram-keyboard" /></td>
<td><ul>
<li><strong>W</strong> : 앞으로 이동</li>
<li><strong>S</strong> : 뒤로 이동</li>
<li><strong>A</strong> : 왼쪽으로 이동</li>
<li><strong>D</strong> : 오른쪽으로 이동</li>
<li><strong>Space</strong> : 위로 이동</li>
<li><strong>Shift</strong> : 아래로 이동</li>
<li><strong>Ctrl</strong> : 이동 가속 (WASD / Space / Shift 와 함께 누름)</li>
<li><strong>F</strong> : 뒤 돌기 (시선 반전)</li>
</ul></td>
</tr>
</table>

### 마우스로 움직이기

<table>
<tr>
<td><img src="https://github.com/user-attachments/assets/b8564a62-b692-4bde-acc3-e67d7794b158" width="320" alt="diagram-mouse-rotate" /></td>
<td><ul>
<li><strong>마우스 이동</strong> : 시선 방향 회전 (시점은 고정, 보는 방향만 회전)</li>
</ul></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/673e077f-a31a-460f-ae5b-d284933b5329" width="320" alt="diagram-zoom" /></td>
<td><ul>
<li><strong>마우스 휠 위</strong> : 줌 인</li>
<li><strong>마우스 휠 아래</strong> : 줌 아웃</li>
</ul></td>
</tr>
</table>

<br />

## 1. 기본 아이디어

- 우리 눈은 **반대편에 가려진 면은 보지 못합니다.** 한 순간에 인식하는 것은 **2차원 정보** 뿐입니다.
- **$n$차원 세계의 관찰자는 매 순간 $(n-1)$차원 도형만 인식** 합니다.
- **3D 도형의 각 점을 2D 평면(화면)에 사영(projection)** 시키면 화면에 그릴 수 있습니다.

<br />

## 2. 원리

### 정사영에서 시점으로

단순 정사영만 쓰면 눈의 위치가 반영되지 않습니다. **시점(관찰자 위치)** 과 **시야각** 을 넣어야 원근이 생성됩니다.

<img src="https://github.com/user-attachments/assets/31f4e7f0-9db7-41bd-8b6d-9afb94e9fba9" width="580" alt="diagram-orthographic" />

**시점을 넣은 모델** 에서는 다음이 핵심입니다.

- **시점 $V$** : 관찰자 위치 (위치벡터 $\vec{v}$)
- **시선벡터 $\vec{p}$** : 시점에서 화면 정중앙점 $C$를 향하는 벡터 (화면에 수직)
- **화면** : 물체의 각 점과 시점을 잇는 직선과 이 평면의 **교점** 이 화면에 그려질 점

<img src="https://github.com/user-attachments/assets/b0d7da38-477e-4d1b-a92c-07711eabb3cd" width="580" alt="diagram-viewpoint" />

즉 **3차원 공간 좌표 → 2차원 평면(화면) 좌표** 로 바꾸는 변환이 필요합니다.

### 좌표 변환 절차

1. 화면 평면의 단위벡터 $\hat{i}'$, $\hat{j}'$ 설정 (시선벡터 $\vec{p}$와 수직)
2. 시점 $V$와 3D 점 $A$를 지나는 직선: $\vec{r}(t) = \vec{v} + t(\vec{a} - \vec{v})$
3. 화면 평면: 법선 $\vec{p}$, 지나는 점 $C$ → $\vec{p} \cdot (\vec{x} - \vec{c}) = 0$
4. 직선과 평면의 **교점 $A'$** 계산
5. 교점이 **선분 $\overline{VA}$ 위** 일 때만 ($0 < t \le 1$) 화면에 그릴 수 있습니다
6. 2D 화면 좌표: $x_{\text{scr}} = (\vec{a}' - \vec{c}) \cdot \hat{i}'$, $y_{\text{scr}} = (\vec{a}' - \vec{c}) \cdot \hat{j}'$ (+ 비율)

<br />

## 3. 구현 요약

구현할 상황을 정리한 것입니다.

<img src="https://github.com/user-attachments/assets/9bb82e29-048f-44f7-a8e3-e808f9eb663a" width="580" alt="diagram-implement" />

### 주요 변수

| 구분 | 의미 | 코드 |
|------|------|------|
| 시점 $V$ | 관찰자 위치 $\vec{v}$ | `Camera.v` |
| 시선벡터 $\vec{p}$ | 시점 → 화면 정중앙, 크기로 줌 조절 | `Camera.p` |
| 화면 법선 $\vec{n}$ | $\vec{p}$ 방향 단위벡터 | `Camera.n` |
| 화면 정중앙 $C$ | $\vec{c} = \vec{v} + \vec{p}$ | `Camera.c` |
| 화면 축 | $\hat{i}'$, $\hat{j}'$ | `Camera.i_prime`, `Camera.j_prime` |

<br />

## 4. 렌더링 대상 (Object)

공통 인터페이스는 `get_coords()`, `get_render_data()` 입니다.

| 클래스 | 설명 | 용도 예 |
|--------|------|---------|
| **Point** | 3D 한 점 | 단일 점, 점군 |
| **RandomPoint** | 구간 내 랜덤 3D 점 | 배경 별 등 |
| **Line** | 두 점을 잇는 선분 | 선, 축 |
| **XAxis / YAxis / ZAxis** | 원점 기준 축 | 좌표축 표시 |
| **Polygon** | 여러 점을 이은 다각형 | 삼각형/사각형 면 |
| **Cube** | 정육면체 (중심, 반지름) | 큐브 |
| **Sphere** | 구 (위도/경도 분할) | 구체 |

<br />

## 5. 실행 방법

### 요구 사항

- Python 3.x
- NumPy
- Pygame

### 설치

```bash
pip install -r requirements.txt
```

### 실행

**메뉴에서 고르기**

```bash
python main.py
```

- 방향키 **↑ / ↓** 로 항목 선택 후 **Enter**, 또는 **1 ~ 7** 번호 입력 후 Enter
- 선택한 도형 데모 창이 실행됩니다.

**도형별로 직접 실행**

```bash
python main_point.py        # 점 (Point)
python main_randompoint.py  # 무작위 점 (RandomPoint)
python main_line.py         # 선 (Line)
python main_polygon.py      # 다각형 (Polygon)
python main_cube.py         # 정육면체 (Cube)
python main_sphere.py       # 구 (Sphere)
python main_mesh.py         # 폴리곤 메쉬 (Polygon Mesh)
```

<br />

이 프로젝트는 3D → 2D 투영과 시점 이동을 **수학적으로 다루고**, **라이브러리 없이 직접 구현** 한 데모입니다.

<br />

## 6. 관련 게시글

더 자세한 수식 및 구현 내용이 궁금하시다면 [블로그 포스팅](https://seungjoonh.tistory.com/entry/project-3d-renderer)을 참고하시면 됩니다.