# [Object] 서브클래싱과 서브타이핑

- 상속의 타입계층의 구현  
-  부모클래스는 일반화 서브클래스는 특수화
- 코드의 재사용

<aside>
💡 객체기반프로그래밍 - 상태와 행동의 캡슐화한 객체의 조합으로 프로그래밍
객체지향프로그래밍 - 객체기반프로그래밍의 일부로, 상속과 다형성을 지원함
#javascript는 프로토타입기반이지만 객체지향언어

</aside>

<aside>
📌 슈퍼타입 - 서브타입이 정의한 퍼블릭인터페이스를 일반화시켜 범용적이고 넓은의미로 정의
서브타입 - 슈퍼타입이 정의한 퍼블릭인터페이스를 특수화시켜 구체적이고 좁은의미로 정의

</aside>

- 상속의조건
- is-a관계를 모델링하는가?
- 부모클래스의 타입으로 자식클래스를 사용해도 무방한가?(대체가능성)
- 펭귄과 새의 관계로 생각해보자
- ISP 인터페이스 분리 원칙
- 서브클래싱 ( 구현상속) , 서브타이핑(인터페이스 상속)
- 리스코프 치환 원칙
- 직사각형과 정사각형, 클라이언트에서 요구하는 직사각형의 역할을 정사각형이 대체할수가 없음. 단순한 서브클래싱이다.
- 즉, 대체가능성(호환성)을 위반하며 리스코프 치환 원칙에 위배된다.
- 이는 현실세계에서의 is-a관계가 프로그래밍 세계에서는 다를 수 있다는 것을 보여준다.
    
    -리스코프 치환원칙은 유연한 설계의 기반이다. (p.459)
    

```java
public class OverlappedDiscountPolicy extends DiscountPolicy{
	private List<DiscountPolicy> discountPolicies = new Array<>();
	public OverlappedDiscountPolicy(DiscountPolicy...discountPolicies){
		this.discountPolicies = Arrays.asList(discountPolicies);
	}
	@Override
	protected Money getDiscountAmount(Screening screening){...}
}
```

- 다음의 코드는 SOLID를 만족하는 대표적인 예이다.
    - 의존성 역전 원칙 → 상위수준의 movie와 하위수준의 overrappedDiscountPolicy는 모두 추상클래스에 의존한다.
    - 리스코프 치환법칙 → 여기서 OverlappedDiscountPolicy는 상위 추상 클래스인 DiscountPolicy를 대체한다.
    - 개방 - 폐쇄 원칙 → 상위 모듈 Movie에 영향을 끼치지 않는다.

### 계약에 의한 설계와 서브타이핑

- 서브타입에 더 강력한 사전 조건을 정의할 수 없다.
- 서브타입에 슈퍼타입과 같거나 더 약한 사전조건을 정의할 수 없다.
- 즉, 부모클래스가 클라이언트와 맺고있는 계약에 관해 깊이있게 고민해야한다.