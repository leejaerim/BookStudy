# [2장 시퀀스]

### 학습 목표

- 리스트부터 문자열 및 파이썬3에 소개된 바이트 자료형까지 시퀀스에 대한 내용을 학습한다.

### 내용

- 컨테이너 시퀀스 - 서로 다른 자료형의 항목을 담을 수 있는, list , tuple, collections.deque 형
- 균일 시퀀스 - 같은 단 하나의 자료형만 담을 수 있는, str, bytes, bytearray, memoryview, array.array형
- 가변성에 대한 분리
    - 가변시퀀스 - 리스트, 바이트어레이, 어레이, 콜렉션, 등
    - 불변 시퀀스 - 튜플, 스트링, 바이트형.
- 지능형 리스트 - 새로운 리스트를 만드는 일을 한다. 단 한줄로 구현하며, 생성된 리스트를 사용하여야 한다.
    - 항목을 필터링 및 변환하여 시퀀스나 기타 반복가능한 자료형으로부터 변환된 리스트를 얻는다.
    - 리스트를 만드는데 특화되어있으며, 다른 종류의 시퀀스로 채우려면 제네레이터 표현식을 사용해야 됨.
- 튜플 언패킹 → 병렬 할당에 사용

```python
lax_coordinates = (33.9425, -118.408056)
latitude , longitude = lax_coordinates # 튜플 언패킹
#튜플 언패킹을 이용한 변수 swap
a, b = b, a
#초과할당에 대한 * 사용
a, b *rest = (1,2,3,4,5) # a= 1, b=2, rest = (3,4,5)
```

---

### 2.4 슬라이싱

- 고급 슬라이싱 형태의 사용법에 대한 학습
- `seq[start : stop : step]` → `seq.__getItem__(slice(start, stop, step))`

---

### 2.7 list.sort()와 sorted() 내장함수

- list.sort() 메서드는 사본을 만들지 않고 리스트 내부에서 변경하여 정렬 → None 객체 반환
    - None을 반환하는 관례는 객체를 직접 변경했다고 노티해주며, 메서드를 연결해서 호출할 수 없다는 단점이 존재.
- 반면, sorted() 내장함수는 아예 새로운 리스트를 생성 하여 반환한다.

---

### 2.8 정렬된 시퀀스를 bisect로 관리하기

```python
import bisect
import sys

def grade(score, breakpoints=[60,70,80,90], grades = 'FDCBA'):
	i = bisect.bisect(breakpoints, score)
	return grades[i]
[grade(score) for score in [33,99,77,70,89,90,100]]
```

- 정렬된 breakpoints 와 같은 숫자 시퀀스를 검색할 때 index보다 더 빠른 bisect 함수를 사용한다.
- `bisect.insert()` 정렬된 상태를 유지하며 인서트
    - `insert(seq, item)` 은 seq를 오름차순으로 유지한채 item을 삽입
    
    ```python
    SIZE = 7
    random.seed(1729)
    my_lists = [] 
    for i in range(SIZE):
    	new_item = random.randrange(SIZE*2)
    	bisect.insert(my_list, new_item)
    	
    ```
    

---

### 2.9 리스트가 답이 아닐 때

- 리스트형이 사용하기 편하고 융통성 있지만, 실수만 저장하는 경우에는 배열이 훨씬 효과적일 수 있다.
- 이와 같이 각 상황에 맞는 시퀀스 형태를 사용하는 것이 중요하다.

1.배열

- 숫자만 존재할 때, array.array
- pop, insert, extend 와 같은 가변시퀀스가 제공하는 모든 연산을 지원한다.
- C 배열만큼 가볍다.
1. 메모리 뷰
    - 공유 메모리 시퀀스형으로 bytes를 복사하지 않으며 배열의 슬라이스를 다룰 수 있게 한다.
2. 덱 및 기타 큐
    - 덱(`collections.deque`) - 양쪽 어디든 빠르게 삽입 및 삭제 가능한 안전한 양방향 큐
    - 덱의 최대길이를 설정할 수 있으면 제한된 상목만 유지할 수 있도록 만든다.
    
    ```python
    from collections import deque
    dq = deque(range(10, maxlen =10)
    dq.rotate(3) # 7 8 9 0 1 2 3 ...
    dq.rotate(-4) # 1,2,3,4,5,6,7...
    dq.appendleft(-1) # -1, 1,2,3,4,5,6,7, , 단 여기서 최 우측은 빠졌다.
    ```
    
    - ***단, 중간항목 연산은 빠르지 않다.  양 끝쪽에서의 연산에 최적화되어 있음.***
    
    ---
    
    ### Heap Q
    
    ```python
    Heapq.heapify()
    Heapq.heappop()
    Heapq.heappush()
    ```
    
    ---