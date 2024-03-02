# [3장] 딕셔너리와 집합

- 고성능 딕셔너리는 해시테이블이라는 엔진을 사용하는데 아주 중요하다.
    - 작동 방식을 공부한다.
        - 키는 반드시 해시 가능해야한다.
        - 동일 객체는 반드시 동일한 해시값.

### 3.2 지능형 딕셔너리

- 튜플리스트를 딕셔너리 생성 코드

```python
DIAL_CODES = [(86,'china'), (91,'India'),...]
#지능형 딕셔너리
country_code = {country: code for code, country in DIAL_CODES}
{code : country.upper() for country, code in country_code.items() ... if code < 66}
```

### 3.4 융통성 있는 키 매핑

- `defaultdict` 존재하지 않는 키에 대한 처리
    - 존재하지 않는 키 인수로 `__getitem__()` 호출마다 기본값 생성하기 위한 콜러블 제공
        - `default_factory` 는 `__getitem__()`을 호출하기 위해 제공 되며, 키가 없을 때 `get()` 을 통해 호출되는 값은 None 객체이다.
        - `__missing__()` 메서드 존재하지 않는 키에 대해 처리
        - `self[key]` 표기법을 이용해서 `__getitem__()` 메서드에 위임.

> Collections.OrderedDict - 키를 삽입한 수서대로 유지함으로써 항목의 반복하는 순서를 예측 가능.
> 
> 
> popitem(last=True)의 형태로 호출하게 되면 처음 삽입한 항목을 꺼낸다.
> 
> collections.ChainMap
> 
> 매핑 목록을 담고 있으며 한꺼번에 검색
> 
> collections.Counter
> 
> 모든 키에 정수형 카운터를 갖고 있는 매핑
> 

```python
ct = collections.Counter('abracadabra')
#ct
# {'a':5,'b':2, 'r':2,'c':1,'d':1}
```

### 3.7 불변 매핑

- `MappingProxyType` 이라는 래퍼 클래스를 제공하여 동적뷰를 제공하되, 불변하도록 만든다.

```python
d = { 1 : 'A'}
d_p = MappingProxyType(d)
d_p[2] = 'B' # Error Raise
d[2] = 'B' # O

```

### 3.8 집합이론

- 집합 SET 은 고유한 객체의 모음으로 중복 항목을 제거

```python
l = [1,1,2,2 ]
set(l) #{1,2}
list(set(l)) # [1,2]
# 교집합 연산
found = len(needles & haystack)
	
```

- 지능형 set

```python
from unicodedata import name
{chr(i) for i in range(32,256) if 'SIGN' in name(chr(i), '') }
```

---

### 해시

- 해시 테이블은 희소배열( 중간에 빈항목을 가진 배열)
- 각 항목별로 버킷이 있고, 버킷에는 키에 대한 참조와 항목의 값에 대한 참조.
- `hash()` 내장 함수 - 두객체가 동일하면 이 값들의 해시값도 동일하다.
- dict의 메모리 오버헤드가 크다.
    - 메모리공간 효율성이 높지 않다.
- 집합의 경우 버킷에는 키에대한 참조가 없다.

---

### 요약

- 기본 dict 외에 defaultdict, OrderedDict, ChainMap, Counter 등 간편한 매핑형 제공
- setdefault(), update() 라는 강력한 메서드 제공
    - 검색 키 존재시 해당키를 가져오고 존재하지 않으면 기본값 해당키를 생성후 기본값 제공
    - 매핑형 반복형 키워드 인수로부터 객체 초기화 하여 대량의 데이터 추가 및 override 가능.
- __missing__()메서드는 키를 찾을수없을때 정의

→ 3,4,5 →  345 → 

hash - > key % 10  ⇒ 1. → 1 → 참조 해쉬  키값을 어떻게 다음 해쉬 알고리즘

충돌 → value + 1  넣는다.  → 2번 일어나게 되면 테이블을 늘린다. 파이썬이

테이블을 미리 만들어놓음 .  11, 3 ,4, 5 , 1

3 ,4 ,5 →  3.5,  11 → 

dict의 키값과 집합에 쓰이는 키값의 객체가 사용하고 있는 타입을 고정하기 위해

불변객체를 씁니다. 가변객체 오브젝트를 쓰게 되면, 해당 오브젝트를 차지하고 있는 주소값의 크기를 제한할 수 없어서 키값으로 사용할 수 없습니다.

 

int → 4 byte 

str → 2bye, or 1byte

hash(key) → hash Key 

key가 위치한 메모리의 주소의 크기가  가변적이면 안됌.