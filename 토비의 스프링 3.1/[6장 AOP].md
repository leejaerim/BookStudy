# [6장 AOP] Aspects Of Programming

<aside>
💡 5장에서 했던 트랜잭션 경계설정을 AOP로 선언하고 깔끔한 방식으로 변경해본다.

</aside>

---

### 트랜잭션 코드의 분리

- 5장에서 UserService에서 비지니스 로직과 트랜잭션의 코드가 공존하고 있다. 이는 상당히 지저분한 코드
- 트랜잭션의 시작과 종료 사이에 비지니스 코드가 존재.
- `UserService` 인터페이스를 만들고, `ServiceImpl` 구상 클래스를 만듦으로써 유연한 확장과 결합도를 낮출 수 있다.
- `UserService` 에는 순수 비지니스 로직만 담고 있는 코드를 남기고, 트랜잭션은 외부로 빼내려고한다.

```java
public interface UserService{
	void add(User user);
	void upgradeLevels();
}
public class UserServiceImpl implements UserService{
	UserDao userDao;
	MailSender mailsender;
	public void upgradeLevels(){...}
}
```

- 단순히 비지니스로직만을 담고 있는 모습
- 분리된 트랜잭션 기능을 담은 `UserServiceTx`

```java
public class UserServiceTx implements UserService{
	UserService userService;
	PlatformTransactionManager transactionManager;
	public void setPlatformTransactionManager...
	public void setUserService(UserService userService){
		this.userService = userService;
	}
	public void add(User user){ userService.add(user);}
	public void upgradeLevels(){
		TransactionStatus status = this.transactionManager.getTransaction
			(new DefaultTransactionDefinition());
		try{
			userService.upgradeLevels();
			this.transactionManager.commit(status);
		}catch(RuntimeException e){
			this.transactionManager.rollback(status);
		}
	}
	
}
```

- Client  → UserServiceTx → UserServiceImpl 순으로 적용

```xml
<bean id="userService"class="...UserServiceTx">
	<property name="transactionManager" ref="transactionManager"/>
	<property name="userService" ref="userServiceImpl"/>
</bean>

<bean id="userServiceImpl" class=".../UserServiceImpl">
	<property name="userDao" ref="userDao">
	<property name="mailSendere" ref="mailSender">
</bean>
```

- UserServiceImpl 코드에서 비지니스로직만 구현할뿐, 트랜잭션과 같은 기술적인 내용은 신경쓰지 않아도 된다.

### 6.2 고립된 단위 테스트

- 단순히 UserService만 테스트 하는 것보다 훨씬 더많은 오브젝트 환경과 서버, 네트워크가 있음.
    - 우리가 의도했던 단위테스트라고 보기 힘듬.
- 6.2.2 테스트 대상 고립 시킬 필요가 있음.
    - 목오브젝트(Stub)을 이용하여 적용한다.
    
    <aside>
    💡 단위 테스트 :  테스트 대상 클래스를 목오브젝트 등의 테스트 대역을 이용해 의존 오브젝트나 외부의 리소스를 사용하지 않도록 고립시켜서 테스트 하는 것.
    통합테스트 : 외부의 리소스가 참여하는 테스트 혹은 두개이상의 성격이나 계층이 다른 오브젝트의 연동 테스트
    
    </aside>
    

### Mockito 프레임 워크

- 목오브젝트의 생성이 매우 귀찮은 작업 → 오히려 배꼽이 더 클 수 있음. 이런 목오브젝트 생성을 도와주는 프레임워크가 존재 ⇒ 바로 Mockito 프레임워크
- `UserDao mockUserDao = mock(UserDao.class);` - 스테틱메소드를 통한 오브젝트 생성
- `when(mockUserDao.getAll()).thenReturn(this.users);` - getAll()메서드 호출시 userList 반환
- `verify(mockUserDao, time(2)).update(any(User.class));` -User타입의 오브젝트를 파라미터로 받아 update() 메소드가 두번 호출됐는지 확인하는 코드
- 다음 네가지로 사용될 수 있다.
    - 인터페이스를 이용한 목 오브젝트의 생성
    - 목오브젝트가 리턴할 값 지정(예외도 가능)
    - 테스트 대상 오브젝트 DI
    - 목오브젝트의 특정메서드 호출 여부 및 어떤 값(파라미터) 호출 검증 가능
- 스프링의 사용은 단위테스트를 만들어야 하고, 목오브젝트는 당연히 필요하다.
    - 이때의 Mockito 프레임워크를 적용할 수 있다.

---

### 6.3 다이내믹 프록시와 팩토리빈

- 핵심기능은 부가기능을 가진 클래스의 존재 자체를 모른다. → ***부가기능이 핵심기능을 사용하는 구조***
    - 부가기능 클래스를 핵심기능을 가진 클래스처럼 꾸며서, 클라이언트에서 사용해야됌.
    - 핵심기능으로 요청과 동시에 자신의 부가기능을 적용
    - ex) 비지니스로직에서의 트랜젝션 기능
- 이 때의 부가기능클래스를 ***프록시(*마치 대리인, 대리자 역할을 수행)***
- 데코레이터 패턴
    - 부가기능을 런타임에 다이내믹하게 부여하기 위한 패턴
    - 프록시로서 동작하는 각 데코레이터 또한 인터페이스로 접근하기 때문에 자신이 최종타깃인지, 다음 단계의 프록시로 위임하는지 알 수 없다.
    - 데코레이터 패턴을 위한 스프링 DI 설정
        
        ```xml
        <bean id="userService" class="spring...UserServiceTx">
        	<property name="transactionManager" ref="transactionManager" />
        	<property name="userService" ref="userSErviceImpl"/>
        </bean>
        
        <!-- 타깃 -->
        <bean id="userServiceImpl" class="...UserServiceImpl">
        	<property name="userDao" ref="userDao"/>
        	<property name="mailSender" ref="mailSender"/>
        </bean>
        ```
        
- 데코레이터 패턴은 타깃의 코드를 손대지 않고, 클라이언트가 호출되는 방법을 손대지않은채, 새로운 기능을 추가할 수있다.
- ***프록시패턴***
    - 클라이언트가 타겟에 접근하는 방식을 변경해준다.(타깃의 기능자체에는 관여 X)
    - 데코레이터와의 차이는, 자신이 만들거나 접근할 타겟클래스를 알고 있다.
    - `java.lang.reflet` 패키지 내부에 프록시를 손쉽게 만드는 지원 클래스가 존재
    
    ```java
    public class UserServiceTx implements UserService{
    	UserService userService; //타깃 오브젝트
    	...
    	public void add(User user){ this.userService.add(user);}	
    	//메소드 구현
    	public void upgradeLevels(){
    		TransactionStatus status = this.transactionManager.getTransaction(new
    			DefaultTransactionDefinition()); //부가기능 수행
    		try{
    			userService.upgradeLevels();//위임
    			this.transactionManager.commit(status);
    		}catch(RuntimeException e){
    			this.transactionManager.rollback(status);
    			throw e;
    		}
    	}
    }
    ```
    
    - 2가지 문제점 존재 : 1. 타깃의 인터페이스 구현 및 위임 번거로움, 2. 중복 가능성
        
        ⇒ 리플렉션 사용. (다이내믹)
        
    
    ```java
    String name = Jaerimlee
    
    Method lengthMethod = String.class.getMethod("length");
    
    //name.length(); 커맨드 패턴.
    int length = lengthMethod.invoke(name); 
    ```
    

---

### 프록시 클래스

- 인터페이스와 타깃 오브젝트

```java
interface Hello{
	String sayHello(String name);
	String sayHi(String name);
	String sayThankyou(String name);
}

public class HelloTarget implement Hello{
	public String sayHello(String name){ return "Hello" + name;}
	public String sayHi(String name){return "Hi"+nanme;}
	...
}
```

- ***프록시클래스***

```java
public class HelloUppercase implements Hello{
	Hello hello ;
	public HelloUppercase(Hello hello){
		this.hello = hello;
	}
	public String sayHello(String name){
		return this.hello.sayHello(name).toUpperCase();
	}
	public String sayHi(String name){
		return this.hello.sayHi(name).toUpperCase();
	}
	public String sayThankyou(String name){
		return this.hello.sayThankyou(name).toUpperCase();
	}
}
```

- 다이나믹 프록시 동작방식 → 프록시 팩토리에 의해 런타임 시 다이내믹하게 만들어지는 오브젝트
- 프록시 팩토리를 사용해, 인터페이스 정보만 주면 인터페이스를 구현한 클래스 오브젝트를 만들어주기 때문,
- 단, 프록시로서 필요한 부가기능 제공코드는 직접 작성해야 한다.
    - 부가기능은 프록시오브젝트와 InvocationHandler를 구현한 오브젝트
    - InvocationHandler오브젝트는 invoke메소드만을 가진 클래스로, 리플랙션 메서드 인터페이스를 파라미터로 받는다.
    - 다이나믹 프록시 → InvocationHandler(invoke()) → TargetObject
    
    ```java
    public class UppercaseHandler implements InvocationHandler{
    	Hello target;
    	public UppercaseHandler(Hello target){this.target = target;}
    	public Object invoke(Object proxy, Method method, Object[] args){
    		String ret = (String)method.invoke(target,args); // 타깃으로 위임, 인터페이스 메소드호출에 적용
    		return ret.toUpperCase(); //부가 기능 제공
    	}
    }
    
    Hello proxiedHello = (Hello)Proxy.newProxyInstance(
    //동적으로 생성되는 다이내믹 프록시 클래스의 로딩에 사용할 클래스 로더, 구현할 인터페이스
    	getClass().getClassLoader(),new Class[] {Hello.Class}, new UppercaseHandler(new HelloTarget()));
    ```
    
    - 클래스 로더 , 인터페이스, InvocationHandler 구현 오브젝트 제공

---