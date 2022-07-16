# [디자인패턴] Singleton Pattern

- 기본적으로 하나의 인스턴스만 제공해야되는 상황에 사용하는 패턴으로
단 하나의 인스턴스만 반환을 보장해야됨.

### Init Pattern

```java
public class Singleton(){
	private static Singleton instance;
	private Singleton(){} //생성자를 통해 다른 소스에서 new를 통한 인스턴스 생성을 방지한다.
	public static synchronized Singleton getInstance(){
		if(instance == null){
			instance = new Singleton();
		}
	}
}
// Singleton.getInstance() 메서드를 통하여 해당 인스턴스를 호출한다.
```

### 멀티 스레드 환경에서의 싱글톤 패턴(이른 초기화 / 더블체킹 방법)

```java
private static final Singleton INSTANCE = new Singleton();
// 다음과 같이 클래스에서 인스턴스를 미리 초기화 시켜버리는 방법이 존재합니다.
// 다만 인스턴스를 만드는 과정이 복잡하거나 리소스를 많이 사용하게 되면,
// 실제로 사용되어지지 않을 경우 리소스를 들고 있게 되는 단점이 존재합니다.
//
private volatile static final Singleton INSTANCE;
public static Singleton getInstance(){
		if(instance == null){
			synchronized(Singleton.class){
				if(instance == null){
					instance = new Singleton();
				}
			}			
		}
	}
//더블체킹의 경우 if문 내부에서 싱크로나이즈드 키워드를 사용하여 멀티스레드 환경에서의
//싱글톤 환경을 제공합니다. 뿐만 아니라 해당 메서드가 호출될때 인스턴스를 초기화하는 좋은 방법입니다.
// 다만 java1.5버전 이상에서 작동되며 다소 복잡해 질 수있다는 단점이 존재합니다.
```

### 최적화 (별도의 holder 이너클래스 구현)

```java
private static class SingletonHolder{
	private static final Singleton INSTANCE= new Singleton();
}
public static Singleton getInstance(){
	return SingletonHolder.INSTANCE;
}
```

### 스프링에서의 싱글톤 패턴

- 스프링에서는 자바빈객체 즉, 스프링 컨테이너를 통하여 싱글톤패턴을 제공한다.
- 별도의 복잡함 없이 우리는 컨테이너에서의 싱글톤 환경을 보장받는다.
- 

---

### 참고자료

`백기선 - 싱글톤 유튜브`