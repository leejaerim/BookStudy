# [CSS Rendering 76강 1회차]

### Graphics System

- Fixed Number *( ABSTRACT CALCULATOR)
    - 환경에 적응이 힘듦, 범용적 사용이 힘듦.
    - %, LEFT, BLOCK, INLINE, FLOAT
- FixedNumber → Abstract CALCULATOR → Componenets → FRAMEWORK

<aside>
📌 서양식 사고 체계 : 상대적인 관점에서 정의하고 확인.

</aside>

### Rendering System

- 보다 구체적이거나 인식하기 쉽게 변환하여 주는 작업 → 랜더링.
- Geometry Calculate → Fragment Fill

### CSS Specifications

- 추상적으로 계산된 체계가 즐비하다. 우리가 원하는 지오메트릭과 프레그먼트를 채우기 위해 CSS 스펙을 정확하게 이해하는 것이 중요하다.
- CSS Level 1  - 기본 사양서
- CSS Level 2 + Module - ms ie4~6 와 각 모듈
- CSS Level 2.1 + 어떤 모듈은 고정된 사양으로 어떤 모듈은 Level 3
- Module Level → Transforms grid flexbox etc…
    - 하나의 브라우저가 모든 모듈의 레벨을 지원하기가 힘듦.
- WICG - Web Platform incubator community group(google)

---

### Normal Flow

- CSS 2.1 Visual Formatting Model
- POSITION
    - ***STATIC | RELATIVE*** | ABSOLUTE | FIXED | INHERIT
- Normal Flow
    - Block Formatting Context | InlineFormatting Context | Relative Formatting Context

---

### Block Formatting Context *(BFC)

- 부모만큼 가로를 전부 가지고 있음. x, y를 부모와 자식 간의 높이와 가로로 공식으로 구할 수 있음.

---

### Inline Formatting Context *(IFC)

- 내용의 width만큼 더해진값이 다음 내용의 x 가 된다.
- 자식의 width의 더한 값이 부모의 width보다 크다면 다음 y로 height 만큼 추가된다.
- HTML 에서 공백이 없는 하나의 문자열은 하나의 IFC로 바라보게 된다.

---

### 예제(그려보고 추측해본다.)

```html
<div style="width:500px">
	**
	<span>
		hello
		<span> World
			<div style="background:red">&nbsp;</div>
		</span>
		!!
		<div style="background:blue">&nbsp;</div>
	</span>
	 **
</div>
<!-- relative는 static을 그리고 상대적인 값만큼 이동시켜 준다. -->
```

---


### Float

- LEFT | RIGHT | NONE | INHERIT
  - NEW BFC
  - FLOAT OVER NORMAL FLOW
  - TEXT, INLINE GUARD
  - ***LINE BOX***
- FLOAT 영역에 대해 새로운 NEW BFC
- ***FLOAT는 INLINE요소에 가드로 작동한다.***
- BLOCK요소는 FLOATTING 될뿐, 영역은 모두 잡힌다.
- LINE 영역은 가용할수 있는 FLOAT 영역만 신경쓴다.  또 가로뿐만 아니라 세로 둘다 기준을 잡는다.

```html
<div style= "width:500px">
	<div class="left" style="width:200px; height:150px">1</div>
	<div class="right" style="width:50px; height:150px">2</div>
	<div class="right" style="width:50px; height:100px">3</div>
	<div class="left" style="width:150px; height:50px">4</div>
	<div class="right" style="width:150px; height:70px">5</div>
	<div class="left" style="width:150px; height:50px">6</div>
	<div class="left" style="width:150px; height:50px">7</div>
	<div style="height:30px;background:red">ABC</div> <!-- Not Float -->
	<!-- ABC 는 인라인 요소로 가드 된다. 블록 자체는 가드 되지 않는다. -->
	<!-- Left 보다 왼쪽을 쓸수없고, Right 보다 오른쪽 영역은 Linebox로 쓸수 없다. -->
</div>
<!-- Linebox 이해 -->
```

---

### OVERFLOW

- VISIBLE | HIDDEN | SCROLL | INHERIT | AUTO(DEFAULT)

### OVERFLOW-X, -Y

- VISIBLE | HIDDEN | SCROLL | CLIP | AUTO

### TEXT-OVERFLOW

- CLIP | ECLIPSIS

<aside>
📌 ***HIDDEN | SCROLL 일때만 값을 갖는 요소로부터 새로운 BFC를 만든다.***

</aside>

- NEW BFC
- FIRST LINE BOX BOUND → 새로운 BFC의 LINEBOX의 BOUND를 갖는다.

```html
<div class="hidden" style="height:30px; background:red">A</div>

<!-- 라인박스를 못잡게 되는 hidden 속성을 가진 div는 히든되어 블록 영역만 가지게 된다. -->
<!-- 라인박스 떄문에 인라인요소가 밀려서 가드 작동하게 되면 블록이 늘어나지 않는다. -->
```

- ***블록으로 생성되지만, 인라인요소로 가드되지 않는 문자열 자체는 밀려나 아예 다른 레이아웃에 위치할 수 있음을 인지한다.***

---

### ***스터디 내용***

[코드스피츠76 - CSS Rendering 1회차 2/2](https://www.youtube.com/watch?v=ybNH1a14vQY&list=PLBNdLLaRx_rKXwi7MulM6v1UG9JLKWIYS&index=2)