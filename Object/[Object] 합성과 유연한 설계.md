# [Object] 합성과 유연한 설계

상속관계 → is - a 관계

합성관계 → has - a 관계

상속관계의 단점 : 자식클래스는 부모클래스의 내부 구현에 열려있음 (결합도의 증가)

합성은 포함된 객체의 퍼블릭 인터페이스를 재사용한다.(구현의 의존성 → 인터페이스 의존성으로 변경)

구현의 대한 결합보다는 인터페이스에대한 결합이 더 좋다.

<aside>
💡 클래스폭발 : 상속의 남용으로 하나의 기능을 추가하기 위해 필요 이상으로 많은 수의 클래스를 추가해야 하는 경우 ( = 조합의 폭발)

</aside>

---

### 합성관계로 변경하기

- 기본 정책 합성하기

```java
public interface RatePolicy{ Money calulateFee(Phone phone}
public class Phone{
	private RatePolicy;
	public Money calulateFee(){
		return ratePolicy.calculateFee(this);
	}
}
# Phone 내부에 RatePolicy에 대한 참조자가 포함되어 있음에 주목하자.
# 런타임 의존성으로 대체하기 위해 RatePolicy인스턴스를 주입받는다.
```

<aside>
💡 Phone phone = new Phone(new RegularPolicy(Money.won(10),Duration.ofSeconds(10))))
런타임 때 동적으로 주입시킨다. (런타임 의존성)

</aside>

### 믹스인

- 객체를 생성할 때 코드 일부를 클래스 안에 섞어 넣어 재사용하는 기법
- 합성처럼 유연하면서도 상속처럼 코드를 재사용할 수 있음.
-