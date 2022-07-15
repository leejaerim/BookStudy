# Template Method Pattern

<aside>
💡 템플릿 메서드 패턴에 대해 공부합니다.

</aside>

```java
abstract class DiscountPolicy{
	private Set<DiscountCondition> conditions = new HashSet<>();
	public void addCondition(DiscountCondition condition){condition.add(condition);}
	public Money calculateFee(Screening screening,int count, Money fee){
		for(DiscountCondition condition : conditions){
			if(condition.isSatisfiedBy(screening, count)) return calculateFee(fee);)
		}
		return fee;
	}
	***protected abstract Money calculateFee(Money money);***
}
```

- OOP를 만족하기 위하여 우리는 다운캐스팅을 하여 사용한다.
    - 예를들어 A라는 클래스를 상속하여 만든 자식클래스 A’가 있다고 가정하여 보자.
    - `A a = new A'()` 를 통해 새로운 인스턴스를 생성하여도, 자식클래스와 상속받은 부모클래스가 한번에 생성된다.
    - 생성된 메모리는 포인터를 통해 관리하게 된다.
    - 여기서 포인터가 부모클래스의 메모리를 가르키게 할지 제어할 수 있도록 만드는 것이 `다운캐스팅` 입니다.
    - 반대로 `A a = new A()` 부모 클래스 인스턴스를 생성한뒤, `(A') a` 와 같이 다운캐스팅하게 된다면, OOP(리스코프 치환원칙)을 위반할 뿐만 아니라 메모리 생성에서도 위험하다. 그렇기 때문에 ***업캐스팅은 지양해야 한다.***
    
- A를 상속한 수많은 자식클래스가 상속받아 구현되었다고 한다면, 수많은 자식클래스가 부모클래스를 바라보고 있고 의존성이 생길 수 밖에 없습니다. (어찌 보면 필수, 당연한 것.)
    - 부모클래스를 수정이라도 한다면 자식클래스 마다 전부 수정을 해줘야 합니다. 
    → OCP원칙에 위배 됩니다.
    - 이럴 때 `템플릿 메서드 패턴` 을 사용합니다. 부모에서 의존성을 역전시켜, 자식클래스가 `protected abstract Money calculateFee(Money money)` 를 구현하도록 시킵니다.
    - 자식 클래스 입장에서는 `calculateFee` 만 구현하며, 그외의 부모 클래스에 대한 지식을 몰라야 합니다.
    - 이렇게 되면 부모클래스 입장에서는 [훅] 을 사용한 템플릿 메서드 패턴으로 의존성을 역전시켜 OCP 원칙에 만족하는 OOP를 달성할 수 있습니다.

```java
public class AmountPolicy extends DiscountPolicy{
	private final Money amount;
	public AmountPolicy(Money amount){
		this.amount = amount
	}
	@Override
	public Money calculateFee(Money Fee){
		return Fee.minus(amount);
	}
}
```

---

### 참고자료

`코드스피치 85강 오브젝트 6회차`