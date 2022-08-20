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