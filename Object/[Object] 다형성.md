# [Object] 다형성

<aside>
💡 목표 : 포함 다형성의 관점에서 런타임에 상속 계층 안에서 적절한 메서드를 선택하는 방법을 이해

</aside>

### 행동관점의 상속

데이터 관점의 상속 → 자식클래스의 인스턴스안에 부모클래스의 인스턴스를 포함

행동관점의 상속 → 부모클래스가 정의한 일부 메서드를 자식클래스의 메서드로 포함

런타임시 , 자식클래스의 정의되지 않은 메서드는 부모클래스안에서 탐색

### 업캐스팅과 동적 바인딩

- 같은 메세지를 받았을 때 다른 메서드
→ Lecture로 인자로 받는 생성자를 만들었다고 하자, 그런데  Lecture를 상속받은 GradeLecture로 인자를 받게 되면 이상없이 실행된다. 동일한 코드 안에서 서로 다른 클래스 안에 구현된 메서드를 실행할수 있음
→ 대체 가능성
- 부모 클래스 타입으로 선언된 변수에 자식클래스의 인스턴스를 할당하는 것 ⇒ 업 캐스팅
- 변수의 타입이 아닌 실행되는 메서드의 따라 결정된다. 컴파일 시점이 아닌, 런타임 시점에서 바인딩 ⇒ 동적바인딩
- 정적바인딩(컴파일타임 바인딩) → 컴파일타임에 호출할 함수를 결정하는 방식
- 동적바인딩(지연바인딩) → 런타임에 실행될 메서드를 결정하는 방식

### 동적메서드 탐색과 다형성

- 자동적인 메세지 위임 → 자식클래스에서 이해할수 없는 메세지 일경우 자동으로 부모클래스에 위임
- self참조를 사용하여 런타임에서 메서드 탐색
- 메서드 오버라이딩도 자식클래스의 우선순위에 밀려서 메시지 처리가 위임되기 때문이다.(부모보다먼저탐색)
→내적동질성
- 이름만 같고 시그니처가 다른, 메서드의 경우 상속이라는 계층에서 공존이 가능한데, 이것이 오버로딩

### 동적인 문맥

- self참조 객체는 동적인 문맥 그 순간의 인스턴스를 참조한다.
    
    → 현재 탐색하고 있는 객체, 메세지를 수신한 객체
    
- 위임 : 자신이 처리할수 없는 요청에 대해 다른 객체에게 동일하게 전달해서 처리를 요청하는 것.
→ 그렇기 때문에 현재의 자기 자신의 참조객체인 self객체를 인자로 같이 넘기게 된다.
    - 반대로 self객체를 인자로 넘기지 않는 포워딩의 경우에는, 코드재사용의 목적으로 메세지 전송하지 않음.

### Prototype Chaining in javascript

- 클래스 기반의 객체지향이 아닌, 프로토타입 기반의 언어인 자바스크립트에서도 자동적인 위임이 일어날수 있다.

```jsx
function Lecture(name, scores) {
	this.name = name;
	this.scores = scores;
}
Lecture.prototype.stats = function(){
	return "Name" + this.name + "Eval Method" + this.getEval();
}
Lecture.prototype.getEval(){ return "Pass or Fail"}

function GradeLecture(name,canceled,scores){
	Lecture.call(this,name,scores) #Binding
	this.canceled = canceled;
}
GradeLecture.prototype = new Lecture();
GradeLecture.prototype.constructor = GradeLecture;
GradeLecture.prototype.getEval = function(){return "Grade"}
#GradeLecture의 프로토타입에 Lecture의 인스턴스가 들어감을 보라.
#이 과정을 통해 GradeLecture를 이용해 생성된 모든 객체들이 prototype을 통해 Lecture에 접근가능
#즉, Lecture의 특성을 상속받았다고 볼 수 있다.
#Lecture 이때의 this는 Lecture가 아닌 GradeLecture를 가르키고 있음을 잊지말자.
```