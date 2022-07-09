# [오브젝트2 84강 1회차]

### 좋은 확장에 대하여

- Super는 나쁘다.
    
    📌 부모의 모든 메소드는 final , private, abstract protected 타입
    📌 부모의 생성자는 인자를 받지 않는다.
    
- Override는 나쁘다. 
- 부모컨텍스트의 모든 지식과 여파를 전부 알수 없기때문에 오버라이딩은 쓰면 안된다고 한다.
📌 부모의 모든 메소드는 final, private, abstract protected 타입

<aside>
💡 그외에 final 키워드를 통하여 class의 확장을 막아줘야 한다.

</aside>

```java
//상속가능한 좋은 형태로 구현
abstract class Plan{
    private Set<Call> calls = new HashSet<>();
    public final void addCall(Call call){ calls.add(call);}
    public final Money calculateFee(){...}
    abstract protected Money calcCallFee(Call call);
}
---
//인터페이스 & 합성로 구현
public interface Calculator{
    Money calculateFee(Call call)
}
public class PricePerTime implements Calculator{
    private final Money price;
    private final Duration second;
    public PricePerTime(Money price, Duration second){...}
    @Override
    public Money calcCallFee(Call call){...}
}
public class Plan{
    private Calculator calc;
    private Set<Call> calls = new HashSet<>();
    public final void addCall(Call call){ calls.add(call);}
		public final  void setCalculator(Calculator calc){...}
    public final Money calculateFee(){...}
    public final Money calcCallFee(){...};
}
```

🐦 ***상속과 합성을 자유자재로 구현할 수 있도록 체화*** 해야한다.