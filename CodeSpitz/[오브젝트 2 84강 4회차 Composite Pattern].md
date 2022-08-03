# [84강 오브젝트 2 Composite Pattern]

```java
public class TaskReport {
	private final CompositeTask task;
	private final List<TaskReport> list = new ArrayList<TaskReport>();
	public TaskReport(CompositeTask task){
		this.task = task;	
	}
	public void add(TaskReport report){
		list.add(report);
	}
	public CompositeTask getTask(){
		return task;
	}
	public List<TaskReport> getList(){
		List<CompositeTask> tasks = new ArrayList<CompositeTask>();
		tasks.sort((a,b) -> type.compare(a,b));
		
		TaskReport report = new TaskReport(this);
		for(CompositeTask t : list){
			report.add(t.getReport(type));
		}
		return report;
	}
}
```

- Task클래스와 Task를 포함하고 있는 Tasks클래스가 존재합니다.
- 이 두가지를 포함할 수 있는 CompositeTask 클래스가 존재합니다.(Composite 객체)
- CompositeTask클래스를 Report 할수있는 TaskReport 클래스가 존재합니다.
    - DI된 CompositeTask의 GetList를 통해 task 내부에 존재하는 모든 서브 트리와 태스크 오브젝트를 list에 담아 반환하여 줍니다.
    - 이는 for문 내에서 오브젝트뿐 아니라 서브트리까지 재귀적으로 작동합니다.

---

- 우리는 이제 `Task` 혹은 `Tasks` 를 `TaskReport` 로 제어할 수 있습니다.
- 그러면 내부 순회하면서 서브트리의 서브트리까지 출력하는 `Renderer` 클래스, 즉 `Visitor` 패턴을 공부합니다.

```java
public class Renderer{
	private final Supplier<Visitor> factory;
	public Renderer(Supplier<Visitor> factory){
		this.factory = factory;
	}
	public void render(TaskReport report){
		redner(factory.get(),report,depth:0);	
	}
	private void render(Visitor visitor, TaskReport report, int Depth){
		visitor.drowTask(report.getTask(),depth);
		for(TaskReport r : report.getList()){
			render(visitor,r,depth:depth+1);
		}
		visitor.end(depth);
	}
}
```

```java
public interface Visitor {
	public void drawTask(CompositeTask task, int depth)
	public void end(int depth)
}
public class ConsoleVisitor implements Visitor{
	@Override
	public void drawTask(CompositeTask task, int depth){
		String padding = "";
		for(int i=0;i<depth;i++){
			padding+="-";
		}
		System.out.println(padding + (task.getIsComplete() ? "[v] " : "[ ] ")
			+ task.getTitle() + "(" + task.getDate() + ")"); 
	}
	@Override
	public void end(int depth){}
}
```

---