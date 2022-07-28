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