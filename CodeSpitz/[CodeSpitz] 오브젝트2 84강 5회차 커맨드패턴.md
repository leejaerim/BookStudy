# [84강 오브젝트 5회차 커맨드패턴]

- Composite Pattern 을 사용하여 오브젝트를 순회하면서 실행시키려고 한다.
- 이때 우리는 커맨드 패턴에 대해 공부하고 적용하고자 한다.

---

- ***커맨드 클래스 인터페이스***

```java
public interface Command{
	public void excute();
	public void undo();
}
```

- 커맨드태스크 클래스

```java
public class CommandTask{
	private CompositeTask task;
	private List<Command> commands = new ArrayList<>();
	public CommandTask(String title, LocalDateTime date){
		this.task = new CompositeTask(title,date);
	}
	private void addCommond(Command cmd){
		commands.add(cmd);
		cmd.excute(task);
	}
	public void toggle(){
		Command cmd = new Toggle();
		addCommand(cmd)
	}
	public void setTitle(String title){
		Command cmd = new Title(title);//함수형 프로그래밍의 클로져처럼 자유변수 역할을 하게 됌
		addCommand(cmd)
	}
	...
}
```

- Toggle 클래스

```java
public class Toggle implement Command{
	@Override
	public void excute(CompositeTask task){
		task.toggle();
	}
	@Override
	public void undo(CompositeTask task){
		task.toggle();
	}
}
```

- Title 클래스

```java
public class Title implement Command{
	private final String title;
	private String oldTitle;
	public Title(String title){
		this.title = title;
	}
	@Override
	public void excute(CompositeTask task){
		oldTitle = task.getTitle();
		task.setTitle(title);
	}
	@Override
	public void unde(CompositeTask task){
		task.setTitle(oldtitle);
	}
}
```

- 이때 필드변수와 같이 인스턴스에서 사용하는 인스턴스 마다의 메모리에 저장되는 변수를 가지는 것을 명심하자.
    - 커맨드태스크 클래스에서 필요한 인스턴스 변수들을 모두 가지게 된다면 불필요한 메모리 낭비 될 수 있다.
- 여기서의 커맨드 패턴은 즉시실행처럼 보일 수 있지만(excute) ***커맨드 패턴의 장점은 실행과 구현을 분리시켜 원하는 시점에 실행할 수 있도록 하는 것이다.***
    - `cmd.excute(task)` 를 원하는 시점에서 호출하게 할 수 있다.(Not in addCommand(…))
- ***Undo와 Redo***

```java
public void redo(){
	if(cursor == commands.size() -1 ) return ;
	commands.get(++cursor).execute(task);
	//변수의 생성없이 이렇게 한줄로 문장을 써둔다는것은 트랜잭션처럼 작동한다고 명시하는 것.
	//커서의 위치가 실행되어진 (addCommand) 위치기 때문에 전위연산자가 사용된 것에 집중
}
public void unde(){
	if (cursor <0) return ;
	commands.get(cursor--).undo(task); 
}
```

- ***addCommand 의 수정(*undo 상태에서의  addCommand시, 이후 서브리스트가 Clear 되어야함)***
    - addCommand를 `public` 으로 선언하며, Command 의 서브클래스 구현 없이 커맨드 패턴을 사용하게 할 수 있다.
    - 대부분의 프레임워크에서 동작하는 커맨드 패턴처럼 메서드를 하나만 갖는 오브젝트를 생성해서 사용할 수 있다.

```java
private void addCommand(Command cmd){
	for(int i = commands.size() -1; i>cursor;){
		commands.remove(i);
	}
	cmd.execute(task);
	commands.add(cmd);
	cursor = commands.size() -1 
	//불변식으로 변경 이때 cursor++ 처럼 후위연산자를 쓴다면 아주 민감하게 상태관리 하여야 한다.
}
```

- ***전략패턴 → 컴포지트 패턴 → 비지터 패턴 → 커맨드패턴 → 메멘토 패턴***
- 전략패턴을 컴포지트 패턴으로 설계하여 관리하고 비지터 패턴으로 독립시켜 커맨드패턴으로 비동기 실행할 수 있도록 하며, 메멘토 패턴으로 상태를 저장 및 관리하고자 한다.

```java
public class CommandTask{
	...
	private final Map<String, String> saved = new HashMap<>();

	public void save(String key){
		JsonVisitor visitor = new JsonVisitor();
		Renderer renderer1 = new Renderer(()->visitor);
		renderer1.render(task.getReport(CompositeSortType.TITLE_ASC));
		saved.put(key,visitor.getJson();
	}
	public void load(String key){
		String json = saved.get(key);
		//SubTask 삭제, jSON 순회 복원
	}
}

```