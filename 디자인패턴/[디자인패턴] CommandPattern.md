# [Command Pattern]

```python
#커맨드 정의
class command():
    def execute(self):
        pass

#execute를 구현하는 상속객체 구현
class Print_command(command):
    def execute(self):
        print("Print Command 입니다")

print_command = Print_command()
print_command.execute()

class Cat():
    def speak(self):
        print("Meou")
    def run(self):
        print("Run")
class CatCommand(command):
    def __init__(self,Cat:Cat, command:command) -> None:
        self.Cat = Cat
        self.Command = command
    def execute(self):
        for command in self.Command:    
            if command == "speak":
                self.Cat.speak()
            if command == "run":
                self.Cat.run()
cat = Cat()
catCommand = CatCommand(cat,['run','speak'])
catCommand.execute()

# invoker 객체
class invoker():
    def __init__(self) -> None:
        self.commandList = []
    def addCommand(self,Command:command):
        self.commandList.append(command)
    def doRun(self):
        for i in self.commandList:
            i.execute()

invoker = invoker()

invoker.addCommand(catCommand)
invoker.addCommand(print_command)

invoker.doRun()
```

### 특징

- 백엔드 환경에서 커맨드 패턴은 가장 기초적이면서 가장 중요하다
- 일반적으로 사용하는 프레임워크*(특히 스프링)에서는 내부적으로 커맨드패턴을 모두 사용한다.
    - 가장 큰 이유는 바로 설계(구현) 시점과 실행 시점을 동적으로 구분할 수 있는데에서 출발한다.
    - 단순하게 구현은 편하게 하지만, 원하는 시점에 해당 명령(Command)을 실행하게 해준다.
    → 지연실행
    - 우리가 원하는 행위들을 서술해두고, 원하는 시점에 일괄 실행할 수 있게 한다.
- 별도의 `invoke` 클래스*(커맨드를 저장하는 객체)를 설정함으로써 구현과 명령의 분리

### 출처

> 코딩없는 프로그래밍 유튜브 - 커맨드 패턴
> 

> 코드스피츠 - 거침없는 자바 스크립트
>